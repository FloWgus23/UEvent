# backend/activities/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
import traceback

# ⭐ เพิ่ม import สำหรับจัดการเวลา
from django.utils import timezone
import datetime

from .models import Activity, Registration, Tag, UserInterest, ActivityTag
from .serializers import (
    ActivitySerializer, 
    ActivityCreateSerializer, 
    ActivityUpdateSerializer,
    RegistrationSerializer,
    TagSerializer,
    UserInterestSerializer,
    BulkUserInterestCreateSerializer,
    UserProfileSerializer
)

# ========================================
# 🔧 UTILITY FUNCTIONS
# ========================================

def update_activity_status_by_time(activity):
    """
    อัพเดทสถานะกิจกรรมตามเวลาจริง
    - ก่อนเวลาเริ่ม → กำลังรับสมัคร
    - ระหว่างเวลา → กำลังดำเนินการ
    - หลังเวลาจบ → สิ้นสุดแล้ว
    """
    now = timezone.now()
    activity_date = activity.date
    
    # ถ้าไม่มีวันที่ ให้เป็น "กำลังรับสมัคร"
    if not activity_date:
        if activity.status != 'กำลังรับสมัคร':
            activity.status = 'กำลังรับสมัคร'
            activity.save(update_fields=['status'])
        return
    
    # สร้าง datetime สำหรับเช็ค
    start_datetime = datetime.datetime.combine(activity_date, activity.start_time or datetime.time(0, 0))
    end_datetime = datetime.datetime.combine(activity_date, activity.end_time or datetime.time(23, 59))
    
    # แปลงเป็น timezone-aware
    start_datetime = timezone.make_aware(start_datetime)
    end_datetime = timezone.make_aware(end_datetime)
    
    # กำหนดสถานะตามเวลา
    if now > end_datetime:
        new_status = 'สิ้นสุดแล้ว'
    elif now >= start_datetime:
        new_status = 'กำลังดำเนินการ'
    else:
        new_status = 'กำลังรับสมัคร'
    
    # อัพเดทถ้าสถานะเปลี่ยน
    if activity.status != new_status:
        activity.status = new_status
        activity.save(update_fields=['status'])


def update_implicit_score(user, activity, score_delta):
    """
    ฟังก์ชันช่วยสำหรับอัปเดตคะแนนความสนใจแบบ Implicit
    เมื่อ User มีปฏิสัมพันธ์กับ Activity (ดู, ลงทะเบียน)
    """
    try:
        tags = activity.tag_list.all()
        for tag in tags:
            interest, created = UserInterest.objects.get_or_create(
                user=user,
                tag=tag,
                defaults={'explicit_score': 0.0, 'implicit_score': 0.0}
            )
            
            # บวกคะแนนเพิ่ม (สูงสุดไม่เกิน 10.0)
            current_score = float(interest.implicit_score)
            new_score = min(current_score + score_delta, 10.0)
            
            interest.implicit_score = new_score
            interest.save()
            
    except Exception as e:
        print(f"⚠️ Failed to update implicit score: {e}")


# ========================================
# 📅 ACTIVITY VIEWSET (Main Logic)
# ========================================

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    permission_classes = [AllowAny]
    
    # ⭐ ปิด Pagination เพื่อให้ Frontend รับข้อมูลได้ง่าย (Array)
    pagination_class = None 
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ActivityCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ActivityUpdateSerializer
        return ActivitySerializer
    
    def get_queryset(self):
        # Prefetch tags เพื่อประสิทธิภาพ
        queryset = Activity.objects.all().prefetch_related('tag_list').order_by('-created_at')
        
        # ---------------------------------------------------------
        # 🔍 1. SMART SEARCH (ค้นหาครอบคลุม)
        # ---------------------------------------------------------
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |           # ชื่อ
                Q(description__icontains=search) |    # รายละเอียด
                Q(location__icontains=search) |       # ⭐ สถานที่
                Q(organizer__icontains=search) |      # ⭐ ผู้จัด
                Q(tag_list__name__icontains=search) | # ⭐ ชื่อแท็ก (เช่น พิมพ์ "Coding" ก็เจอ)
                Q(tags__icontains=search)             # แท็กเก่า
            ).distinct()

        # ---------------------------------------------------------
        # 🏷️ 2. ADVANCED FILTERS
        # ---------------------------------------------------------
        
        # กรองหลายแท็กพร้อมกัน (Multi-Tag ID) เช่น ?tag_ids=1,5
        tag_ids = self.request.query_params.get('tag_ids', None)
        if tag_ids:
            try:
                ids = [int(x) for x in tag_ids.split(',') if x.isdigit()]
                if ids:
                    queryset = queryset.filter(tag_list__id__in=ids).distinct()
            except ValueError:
                pass
        
        # กรองแท็กเดียว (Legacy)
        tag_single = self.request.query_params.get('tag', None)
        if tag_single:
            queryset = queryset.filter(
                Q(tags__icontains=tag_single) |
                Q(tag_list__name__icontains=tag_single)
            ).distinct()

        # กรองหมวดหมู่
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # กรองช่วงเวลา
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        # กรองสถานะ
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset
    
    # ⭐ Override list เพื่ออัพเดทสถานะก่อนส่งข้อมูล
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # อัพเดทสถานะทุกกิจกรรมก่อนส่ง
        for activity in queryset:
            update_activity_status_by_time(activity)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    # ⭐ Override retrieve เพื่ออัพเดทสถานะก่อนส่งข้อมูล
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        update_activity_status_by_time(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    # ⭐ Override create เพื่อบันทึก owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    # ---------------------------------------------------------
    # ⚡ ACTIONS (Register, Log View, etc.)
    # ---------------------------------------------------------

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        """ลงทะเบียนเข้าร่วมกิจกรรม"""
        activity = self.get_object()
        
        # ========================================================
        # ⭐ เช็คว่าผู้ใช้เป็นเจ้าของกิจกรรมหรือไม่
        # ========================================================
        if activity.owner == request.user:
            return Response({
                'error': 'คุณเป็นผู้จัดกิจกรรมนี้ ไม่สามารถลงทะเบียนเข้าร่วมได้'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ========================================================
        # ⭐ ส่วนที่เพิ่มใหม่: เช็คว่ากิจกรรมจบหรือยัง?
        # ========================================================
        # 1. เช็คจากสถานะ (ถ้าแอดมินปรับเป็น 'สิ้นสุดแล้ว')
        if activity.status == 'สิ้นสุดแล้ว':
             return Response({'error': 'กิจกรรมนี้สิ้นสุดแล้ว ไม่สามารถลงทะเบียนได้'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. เช็คจากวันเวลาจริง (Real-time check)
        try:
            # รวมวันที่ (date) และเวลาสิ้นสุด (end_time) เข้าด้วยกัน
            # ถ้าไม่มี end_time ให้ถือว่าจบตอน 23:59:59 ของวันนั้น
            end_t = activity.end_time or datetime.time(23, 59, 59)
            activity_end_datetime = datetime.datetime.combine(activity.date, end_t)
            
            # ทำให้เป็น timezone aware (เพื่อให้เทียบกับ timezone.now() ได้ถูกต้อง)
            if timezone.is_naive(activity_end_datetime):
                activity_end_datetime = timezone.make_aware(activity_end_datetime)
            
            # ถ้าเวลาปัจจุบัน เลยเวลาสิ้นสุดไปแล้ว
            if timezone.now() > activity_end_datetime:
                return Response({'error': 'กิจกรรมนี้สิ้นสุดระยะเวลาลงทะเบียนแล้ว'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            print(f"Error checking time: {e}")
            # ถ้าคำนวณเวลาผิดพลาด ปล่อยผ่านไปก่อน หรือ handle ตามสมควร
            pass
        # ========================================================
        
        # Validation
        if Registration.objects.filter(user=request.user, activity=activity).exists():
            return Response({'error': 'คุณได้ลงทะเบียนกิจกรรมนี้แล้ว'}, status=status.HTTP_400_BAD_REQUEST)
        
        if activity.registered_count >= activity.capacity:
            return Response({'error': 'กิจกรรมเต็มแล้ว'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create Registration
        registration = Registration.objects.create(
            user=request.user, 
            activity=activity,
            phone=request.data.get('phone', ''), 
            note=request.data.get('note', '')
        )
        
        # Update Count
        activity.registered_count += 1
        activity.save()
        
        # ⭐ IMPLICIT FEEDBACK: ลงทะเบียน = สนใจมาก (+3.0 คะแนน)
        update_implicit_score(request.user, activity, 3.0)
        
        serializer = RegistrationSerializer(registration, context={'request': request})
        return Response({'message': 'ลงทะเบียนสำเร็จ', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def log_view(self, request, pk=None):
        """
        ⭐ บันทึกการเข้าชม (Implicit Feedback)
        เมื่อ User กดดูรายละเอียดกิจกรรม ให้บวกคะแนนความสนใจเล็กน้อย (+0.2)
        """
        activity = self.get_object()
        update_implicit_score(request.user, activity, 0.2)
        return Response({'message': 'View logged'})

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def check_registration(self, request, pk=None):
        activity = self.get_object()
        is_registered = Registration.objects.filter(user=request.user, activity=activity).exists()
        return Response({'is_registered': is_registered})

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unregister(self, request, pk=None):
        activity = self.get_object()
        try:
            registration = Registration.objects.get(user=request.user, activity=activity)
            registration.delete()
            
            activity.registered_count = max(0, activity.registered_count - 1)
            activity.save()
            
            # ⭐ IMPLICIT FEEDBACK: ยกเลิก = ความสนใจลดลง (-1.0 คะแนน)
            update_implicit_score(request.user, activity, -1.0)
            
            return Response({'message': 'ยกเลิกการลงทะเบียนสำเร็จ'})
        except Registration.DoesNotExist:
            return Response({'error': 'ไม่พบข้อมูลการลงทะเบียน'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        activity = self.get_object()
        registrations = Registration.objects.filter(activity=activity)
        serializer = RegistrationSerializer(registrations, many=True, context={'request': request})
        return Response(serializer.data)

    # ⭐ เพิ่ม Custom Action: ดึงกิจกรรมที่ตัวเองสร้าง
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_activities(self, request):
        """
        ดึงเฉพาะกิจกรรมที่ User ปัจจุบันเป็นคนสร้าง
        สำหรับหน้า Organizer Dashboard
        """
        activities = Activity.objects.filter(owner=request.user).prefetch_related('tag_list').order_by('-created_at')
        
        # ⭐ อัพเดทสถานะทุกกิจกรรมก่อนส่ง
        for activity in activities:
            update_activity_status_by_time(activity)
        
        serializer = ActivitySerializer(activities, many=True, context={'request': request})
        return Response(serializer.data)


# ========================================
# 👤 USER PROFILE & TAG SYSTEM
# ========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_profile(request):
    serializer = UserProfileSerializer(request.user, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_tags(request):
    """ดึง Tags ทั้งหมด"""
    try:
        tags = Tag.objects.filter(is_active=True).order_by('name')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_interests(request):
    """จัดการความสนใจของผู้ใช้"""
    if request.method == 'GET':
        interests = UserInterest.objects.filter(user=request.user)
        serializer = UserInterestSerializer(interests, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BulkUserInterestCreateSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            interests = serializer.save()
            result_serializer = UserInterestSerializer(interests, many=True)
            return Response({
                'message': f'บันทึกสำเร็จ {len(interests)} รายการ',
                'data': result_serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_has_interests(request):
    has_interests = UserInterest.objects.filter(user=request.user).exists()
    return Response({'has_interests': has_interests})


# ========================================
# 🧠 RECOMMENDATION SYSTEM (Hybrid)
# ========================================

@api_view(['GET'])
@permission_classes([AllowAny])
def recommended_activities(request):
    """
    ระบบแนะนำกิจกรรม:
    1. ถ้า Guest -> ส่ง Popular
    2. ถ้า Member แต่ไม่มี Interest -> ส่ง Popular
    3. ถ้า Member และมี Interest -> ส่ง Personalized (Content-Based + Weighted Score)
    """
    
    def get_popular_activities():
        return Activity.objects.filter(
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']
        ).order_by('-created_at', '-registered_count')[:20]

    try:
        # Case 1: Guest
        if not request.user.is_authenticated:
            activities = get_popular_activities()
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response({
                'activities': serializer.data,
                'recommendation_type': 'popular',
                'has_interests': False,
                'message': 'กิจกรรมล่าสุด (สำหรับบุคคลทั่วไป)'
            })

        # Case 2: Member
        user = request.user
        user_interests = UserInterest.objects.filter(user=user)
        
        # ถ้ายังไม่เลือกความสนใจ
        if not user_interests.exists():
            activities = get_popular_activities()
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response({
                'activities': serializer.data,
                'recommendation_type': 'popular',
                'has_interests': False,
                'message': 'กิจกรรมแนะนำ (ยังไม่ได้เลือกความสนใจ)'
            })
        
        # คำนวณคะแนน (Weighted Score)
        interested_tag_ids = list(user_interests.values_list('tag_id', flat=True))
        
        matching_activities = Activity.objects.filter(
            tag_list__id__in=interested_tag_ids,
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']
        ).distinct()
        
        activities_with_score = []
        for activity in matching_activities:
            activity_tag_ids = set(activity.tag_list.values_list('id', flat=True))
            matched_tags = set(interested_tag_ids) & activity_tag_ids
            
            if not matched_tags: continue
            
            # รวมคะแนน Total Score (Explicit 70% + Implicit 30%)
            total_score = 0
            for tid in matched_tags:
                interest = user_interests.get(tag_id=tid)
                total_score += interest.total_score
            
            max_possible = len(matched_tags) * 10
            match_score = (total_score / max_possible) if max_possible > 0 else 0
            
            activities_with_score.append({
                'activity': activity,
                'match_score': round(match_score, 2),
                'matched_tags': len(matched_tags)
            })
        
        # Case 3: Fallback (ถ้าคำนวณแล้วไม่เจอ)
        if not activities_with_score:
            activities = get_popular_activities()
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response({
                'activities': serializer.data,
                'recommendation_type': 'popular_fallback',
                'has_interests': True,
                'message': 'ไม่พบกิจกรรมที่ตรงกับความสนใจ (แสดงกิจกรรมล่าสุดแทน)'
            })

        # เรียงตามคะแนนความตรงใจ
        activities_with_score.sort(key=lambda x: x['match_score'], reverse=True)
        top_activities = activities_with_score[:20]
        
        result = []
        for item in top_activities:
            data = ActivitySerializer(item['activity'], context={'request': request}).data
            data['match_score'] = item['match_score']
            result.append(data)
        
        return Response({
            'activities': result,
            'recommendation_type': 'personalized',
            'has_interests': True,
            'message': None
        })
        
    except Exception as e:
        print(f"❌ Error in recommended_activities: {e}")
        traceback.print_exc()
        
        # Emergency Fallback
        activities = get_popular_activities()
        serializer = ActivitySerializer(activities, many=True, context={'request': request})
        return Response({
            'activities': serializer.data,
            'recommendation_type': 'error_fallback',
            'has_interests': False,
            'message': f'เกิดข้อผิดพลาด: {str(e)}'
        })
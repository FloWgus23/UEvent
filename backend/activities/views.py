# backend/activities/views.py (IMPROVED VERSION - SAFE FOR DEMO)
# ✅ แก้ไขเฉพาะ Logic ไม่ต้องแตะ Models หรือ Database
# ✅ ใช้งานได้ทันทีโดยไม่ต้อง migrate

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Q, Count, Prefetch
from django.shortcuts import get_object_or_404
import traceback
import random

# ⭐ เพิ่ม import สำหรับจัดการเวลา
from django.utils import timezone
import datetime
from datetime import timedelta

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


def calculate_time_decay_factor(last_updated):
    """
    🆕 คำนวณค่า Decay ตามเวลา (ไม่ต้องแก้ Model)
    - ล่าสุด 0-30 วัน = 1.0 (คะแนนเต็ม)
    - 31-90 วัน = 0.9
    - 91-180 วัน = 0.7
    - 181-365 วัน = 0.5
    - >365 วัน = 0.3
    """
    if not last_updated:
        return 0.5  # Default ถ้าไม่มีข้อมูล
    
    days_ago = (timezone.now() - last_updated).days
    
    if days_ago <= 30:
        return 1.0
    elif days_ago <= 90:
        return 0.9
    elif days_ago <= 180:
        return 0.7
    elif days_ago <= 365:
        return 0.5
    else:
        return 0.3


def update_implicit_score(user, activity, interaction_type):
    """
    🔧 IMPROVED: ฟังก์ชันอัปเดตคะแนนความสนใจแบบ Implicit
    
    interaction_type:
    - 'view': ดูกิจกรรม → +0.5 คะแนน
    - 'register': ลงทะเบียน → +2.5 คะแนน (เพิ่มจาก 2.0)
    - 'unregister': ยกเลิก → -1.5 คะแนน (เพิ่มจาก -1.0)
    
    ✅ เพิ่ม Cap ที่ 10.0 เพื่อไม่ให้คะแนนพุ่งเกินไป
    ✅ ไม่ให้ติดลบ (ขั้นต่ำ 0.0)
    """
    try:
        tags = activity.tag_list.all()
        
        # กำหนดค่าคะแนนตาม interaction
        score_map = {
            'view': 0.5,
            'register': 2.5,
            'unregister': -1.5
        }
        
        score_delta = score_map.get(interaction_type, 0)
        
        for tag in tags:
            interest, created = UserInterest.objects.get_or_create(
                user=user,
                tag=tag,
                defaults={'explicit_score': 0.0, 'implicit_score': 0.0}
            )
            
            # คำนวณคะแนนใหม่
            current_score = float(interest.implicit_score)
            new_score = current_score + score_delta
            
            # ✅ Cap: ไม่เกิน 10.0 และไม่ติดลบ
            new_score = max(0.0, min(new_score, 10.0))
            
            interest.implicit_score = new_score
            interest.save(update_fields=['implicit_score', 'last_updated'])
            
            print(f"✅ {user.username} - {tag.name}: {interaction_type} → {current_score:.1f} → {new_score:.1f}")
            
    except Exception as e:
        print(f"⚠️ Failed to update implicit score: {e}")
        traceback.print_exc()


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
        """
        🔧 IMPROVED: เพิ่ม Prefetch เพื่อแก้ N+1 Query Problem
        """
        # ✅ Prefetch tags เพื่อประสิทธิภาพ (แก้ N+1 Query)
        queryset = Activity.objects.all().prefetch_related(
            Prefetch('tag_list', queryset=Tag.objects.all())
        ).order_by('-created_at')
        
        # ---------------------------------------------------------
        # 🔍 1. SMART SEARCH (ค้นหาครอบคลุม)
        # ---------------------------------------------------------
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |           # ชื่อ
                Q(description__icontains=search) |    # รายละเอียด
                Q(location__icontains=search) |       # สถานที่
                Q(organizer__icontains=search) |      # ผู้จัด
                Q(tag_list__name__icontains=search) | # ชื่อแท็ก
                Q(tags__icontains=search)             # แท็กเก่า
            ).distinct()

        # ---------------------------------------------------------
        # 🏷️ 2. ADVANCED FILTERS
        # ---------------------------------------------------------
        
        # กรองหลายแท็กพร้อมกัน
        tag_ids = self.request.query_params.get('tag_ids', None)
        if tag_ids:
            try:
                ids = [int(x) for x in tag_ids.split(',') if x.isdigit()]
                if ids:
                    queryset = queryset.filter(tag_list__id__in=ids).distinct()
            except ValueError:
                pass
        
        # กรองแท็กเดียว
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
        
        # 🆕 บันทึก Log View (Implicit Feedback)
        if request.user.is_authenticated:
            update_implicit_score(request.user, instance, 'view')
        
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
        
        # เช็คว่าผู้ใช้เป็นเจ้าของกิจกรรมหรือไม่
        if activity.owner == request.user:
            return Response({
                'error': 'คุณไม่สามารถลงทะเบียนกิจกรรมของตัวเองได้',
                'code': 'OWNER_CANNOT_REGISTER'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # เช็คว่ากิจกรรมยังรับสมัครอยู่หรือไม่
        if activity.status != 'กำลังรับสมัคร':
            return Response({
                'error': 'กิจกรรมนี้ไม่เปิดรับสมัครแล้ว',
                'code': 'NOT_ACCEPTING_REGISTRATION'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # เช็คว่าลงทะเบียนซ้ำหรือไม่
        if Registration.objects.filter(user=request.user, activity=activity).exists():
            return Response({
                'error': 'คุณได้ลงทะเบียนกิจกรรมนี้แล้ว',
                'code': 'ALREADY_REGISTERED'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # เช็คว่ากิจกรรมเต็มหรือไม่
        if activity.registered_count >= activity.capacity:
            return Response({
                'error': 'กิจกรรมเต็มแล้ว',
                'code': 'ACTIVITY_FULL'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # สร้างการลงทะเบียน
        try:
            registration = Registration.objects.create(
                user=request.user,
                activity=activity,
                phone=request.data.get('phone', ''),
                note=request.data.get('note', '')
            )
            
            # เพิ่มจำนวนคนลงทะเบียน
            activity.registered_count += 1
            activity.save(update_fields=['registered_count'])
            
            # 🆕 IMPLICIT FEEDBACK: ลงทะเบียน = ความสนใจสูง (+2.5 คะแนน)
            update_implicit_score(request.user, activity, 'register')
            
            serializer = RegistrationSerializer(registration, context={'request': request})
            return Response({
                'message': 'ลงทะเบียนสำเร็จ',
                'registration': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'เกิดข้อผิดพลาด: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def check_registration(self, request, pk=None):
        """เช็คว่าลงทะเบียนหรือยัง"""
        activity = self.get_object()
        is_registered = Registration.objects.filter(
            user=request.user, 
            activity=activity
        ).exists()
        return Response({'is_registered': is_registered})

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unregister(self, request, pk=None):
        """ยกเลิกการลงทะเบียน"""
        activity = self.get_object()
        
        try:
            registration = Registration.objects.get(
                user=request.user, 
                activity=activity
            )
            registration.delete()
            
            activity.registered_count = max(0, activity.registered_count - 1)
            activity.save(update_fields=['registered_count'])
            
            # 🆕 IMPLICIT FEEDBACK: ยกเลิก = ความสนใจลดลง (-1.5 คะแนน)
            update_implicit_score(request.user, activity, 'unregister')
            
            return Response({'message': 'ยกเลิกการลงทะเบียนสำเร็จ'})
        except Registration.DoesNotExist:
            return Response({'error': 'ไม่พบข้อมูลการลงทะเบียน'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        activity = self.get_object()
        registrations = Registration.objects.filter(activity=activity)
        serializer = RegistrationSerializer(registrations, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_activities(self, request):
        """
        ดึงเฉพาะกิจกรรมที่ User ปัจจุบันเป็นคนสร้าง
        สำหรับหน้า Organizer Dashboard
        """
        activities = Activity.objects.filter(
            owner=request.user
        ).prefetch_related('tag_list').order_by('-created_at')
        
        # อัพเดทสถานะทุกกิจกรรมก่อนส่ง
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
# 🧠 RECOMMENDATION SYSTEM (IMPROVED)
# ========================================

@api_view(['GET'])
@permission_classes([AllowAny])
def recommended_activities(request):
    """
    🔧 IMPROVED RECOMMENDATION SYSTEM:
    
    1. Guest → ส่ง Popular
    2. Member ไม่มี Interest → ส่ง Popular
    3. Member มี Interest → ส่ง Personalized (Content-Based)
    
    ✅ เพิ่ม Time Decay (คะแนนเก่าจะลดลง)
    ✅ เพิ่ม Diversity (80% Personalized + 20% Random)
    ✅ แก้ Performance (ใช้ Prefetch)
    """
    
    def get_popular_activities():
        """ดึงกิจกรรมยอดนิยม (ล่าสุด + คนลงทะเบียนเยอะ)"""
        return Activity.objects.filter(
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']
        ).prefetch_related('tag_list').order_by('-created_at', '-registered_count')[:20]

    try:
        # ========================================
        # CASE 1: GUEST USER
        # ========================================
        if not request.user.is_authenticated:
            activities = get_popular_activities()
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response({
                'activities': serializer.data,
                'recommendation_type': 'popular',
                'has_interests': False,
                'message': 'กิจกรรมล่าสุด (สำหรับบุคคลทั่วไป)'
            })

        # ========================================
        # CASE 2: MEMBER WITHOUT INTERESTS
        # ========================================
        user = request.user
        user_interests = UserInterest.objects.filter(user=user).select_related('tag')
        
        if not user_interests.exists():
            activities = get_popular_activities()
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response({
                'activities': serializer.data,
                'recommendation_type': 'popular',
                'has_interests': False,
                'message': 'กิจกรรมแนะนำ (ยังไม่ได้เลือกความสนใจ)'
            })
        
        # ========================================
        # CASE 3: PERSONALIZED RECOMMENDATION
        # ========================================
        
        # 🆕 คำนวณคะแนนพร้อม Time Decay
        interests_with_decay = []
        for interest in user_interests:
            decay_factor = calculate_time_decay_factor(interest.last_updated)
            
            # คำนวณ Total Score (Explicit 70% + Implicit 30%) * Decay
            base_score = (0.7 * float(interest.explicit_score)) + (0.3 * float(interest.implicit_score))
            final_score = base_score * decay_factor
            
            interests_with_decay.append({
                'tag_id': interest.tag_id,
                'score': final_score,
                'decay': decay_factor
            })
        
        # เรียงตามคะแนนจากมากไปน้อย
        interests_with_decay.sort(key=lambda x: x['score'], reverse=True)
        interested_tag_ids = [item['tag_id'] for item in interests_with_decay]
        
        # ✅ ใช้ Prefetch เพื่อแก้ N+1 Query
        matching_activities = Activity.objects.filter(
            tag_list__id__in=interested_tag_ids,
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']
        ).prefetch_related('tag_list').distinct()
        
        # คำนวณคะแนนความตรงกับความสนใจ
        activities_with_score = []
        
        for activity in matching_activities:
            # ✅ ใช้ค่าที่ prefetch แล้ว (ไม่มี Query เพิ่ม)
            activity_tag_ids = {tag.id for tag in activity.tag_list.all()}
            matched_tag_ids = set(interested_tag_ids) & activity_tag_ids
            
            if not matched_tag_ids:
                continue
            
            # รวมคะแนนจาก Tags ที่ตรงกัน
            total_score = 0
            for tid in matched_tag_ids:
                # หาคะแนนจาก interests_with_decay
                for item in interests_with_decay:
                    if item['tag_id'] == tid:
                        total_score += item['score']
                        break
            
            # Normalize score (0-1)
            max_possible = len(matched_tag_ids) * 10  # แต่ละ tag สูงสุด 10 คะแนน
            match_score = (total_score / max_possible) if max_possible > 0 else 0
            
            activities_with_score.append({
                'activity': activity,
                'match_score': round(match_score, 2),
                'matched_tags': len(matched_tag_ids)
            })
        
        # ========================================
        # FALLBACK: ถ้าไม่เจอกิจกรรมที่ตรงใจ
        # ========================================
        if not activities_with_score:
            activities = get_popular_activities()
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response({
                'activities': serializer.data,
                'recommendation_type': 'popular_fallback',
                'has_interests': True,
                'message': 'ไม่พบกิจกรรมที่ตรงกับความสนใจ (แสดงกิจกรรมล่าสุดแทน)'
            })

        # ========================================
        # 🆕 DIVERSITY: 80% Personalized + 20% Random
        # ========================================
        
        # เรียงตามคะแนน
        activities_with_score.sort(key=lambda x: (-x['match_score'], -x['matched_tags']))
        
        # แบ่งเป็น 80% Personalized
        personalized_count = max(1, int(len(activities_with_score) * 0.8))
        personalized_activities = activities_with_score[:personalized_count]
        
        # เพิ่ม 20% Random (สำหรับ Exploration)
        used_activity_ids = {item['activity'].id for item in personalized_activities}
        
        random_activities = Activity.objects.filter(
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']
        ).exclude(
            id__in=used_activity_ids
        ).prefetch_related('tag_list').order_by('?')[:5]  # สุ่ม 5 กิจกรรม
        
        # รวมกัน
        for activity in random_activities:
            activities_with_score.append({
                'activity': activity,
                'match_score': 0.0,
                'matched_tags': 0
            })
        
        # Shuffle เล็กน้อย (เว้น Top 3)
        top_3 = personalized_activities[:3]
        rest = personalized_activities[3:] + [
            {'activity': act, 'match_score': 0.0, 'matched_tags': 0}
            for act in random_activities
        ]
        random.shuffle(rest)
        
        final_list = top_3 + rest
        final_list = final_list[:20]  # จำกัดแค่ 20 กิจกรรม
        
        # ========================================
        # SERIALIZE RESULT
        # ========================================
        result = []
        for item in final_list:
            data = ActivitySerializer(item['activity'], context={'request': request}).data
            data['match_score'] = item['match_score']
            data['matched_tags'] = item['matched_tags']
            result.append(data)
        
        return Response({
            'activities': result,
            'recommendation_type': 'personalized',
            'has_interests': True,
            'message': None,
            'debug_info': {
                'total_interests': len(user_interests),
                'personalized_count': len(personalized_activities),
                'random_count': len(random_activities),
                'top_tags': [item['tag_id'] for item in interests_with_decay[:5]]
            }
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
    

# ========================================
# 📊 ORGANIZER DASHBOARD STATISTICS
# ========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_faculty_statistics(request):
    """
    ดึงสถิติสัดส่วนผู้ลงทะเบียนตามคณะ
    สำหรับผู้จัดกิจกรรม (Organizer) เท่านั้น
    """
    # ⭐ Dictionary แปลงค่าคณะจากภาษาอังกฤษเป็นไทย
    FACULTY_MAPPING = {
        'science': 'คณะวิทยาศาสตร์',
        'engineering': 'คณะวิศวกรรมศาสตร์',
        'business': 'คณะบริหารศาสตร์',
        'liberal_arts': 'คณะศิลปศาสตร์',
        'agriculture': 'คณะเกษตรศาสตร์',
        'nursing': 'คณะพยาบาลศาสตร์',
        'pharmacy': 'คณะเภสัชศาสตร์',
        'law': 'คณะนิติศาสตร์',
        'political': 'คณะรัฐศาสตร์',
        'other': 'อื่นๆ',
        None: 'ไม่ระบุคณะ',
        '': 'ไม่ระบุคณะ'
    }
    
    try:
        # ⭐ แก้ไข: เช็คจาก Profile แทน User
        try:
            organizer_status = request.user.profile.organizer_status
            if organizer_status != 'approved':
                print(f"❌ User {request.user.username} is not approved organizer (status: {organizer_status})")
                return Response({"error": "Not authorized - Organizer not approved"}, status=403)
        except AttributeError:
            print(f"❌ User {request.user.username} has no organizer_status")
            return Response({"error": "Not authorized - No organizer status"}, status=403)
        
        print(f"✅ User {request.user.username} is approved organizer")
        
        # ดึงกิจกรรมของ organizer คนนี้
        my_activities = Activity.objects.filter(owner=request.user)
        print(f"📊 Found {my_activities.count()} activities")
        
        if my_activities.count() == 0:
            return Response({
                'labels': ['ยังไม่มีกิจกรรม'],
                'data': [0]
            })
        
        # นับจำนวนผู้ลงทะเบียนแต่ละคณะ
        faculty_stats = Registration.objects.filter(
            activity__in=my_activities
        ).values(
            'user__profile__faculty'
        ).annotate(
            count=Count('id')
        ).order_by('-count')
        
        print(f"📊 Faculty stats raw: {list(faculty_stats)}")
        
        # จัดรูปแบบข้อมูล และแปลงเป็นภาษาไทย
        labels = []
        data = []
        
        for stat in faculty_stats:
            faculty_code = stat['user__profile__faculty']
            # ⭐ แปลงเป็นภาษาไทย
            faculty_name = FACULTY_MAPPING.get(faculty_code, faculty_code or 'ไม่ระบุคณะ')
            labels.append(faculty_name)
            data.append(stat['count'])
        
        # ถ้าไม่มีข้อมูลเลย ให้ส่ง fallback
        if not labels:
            return Response({
                'labels': ['ยังไม่มีผู้ลงทะเบียน'],
                'data': [0]
            })
        
        print(f"✅ Faculty Statistics: {dict(zip(labels, data))}")
        
        return Response({
            'labels': labels,
            'data': data
        })
        
    except Exception as e:
        print(f"❌ Error in faculty statistics: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'labels': ['เกิดข้อผิดพลาด'],
            'data': [1]
        }, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_registration_trend(request):
    """
    ดึงแนวโน้มการลงทะเบียน 7 วันล่าสุด
    สำหรับผู้จัดกิจกรรม (Organizer Dashboard)
    """
    try:
        # ⭐ แก้ไข: เช็คจาก Profile แทน User
        try:
            organizer_status = request.user.profile.organizer_status
            if organizer_status != 'approved':
                print(f"❌ User {request.user.username} is not approved organizer (status: {organizer_status})")
                return Response({"error": "Not authorized - Organizer not approved"}, status=403)
        except AttributeError:
            print(f"❌ User {request.user.username} has no organizer_status")
            return Response({"error": "Not authorized - No organizer status"}, status=403)
        
        print(f"✅ User {request.user.username} is approved organizer")
        
        # คำนวณ 7 วันย้อนหลัง
        today = timezone.now().date()
        labels = []
        data = []
        
        # ชื่อวันภาษาไทย
        thai_days = ['จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.', 'อา.']
        
        for i in range(6, -1, -1):  # 7 วันย้อนหลัง
            target_date = today - timedelta(days=i)
            
            # นับจำนวนการลงทะเบียนในวันนั้น
            count = Registration.objects.filter(
                activity__owner=request.user,  # เฉพาะกิจกรรมของตัวเอง
                registered_at__date=target_date
            ).count()
            
            # ใช้ชื่อวันภาษาไทย
            day_name = thai_days[target_date.weekday()]
            labels.append(day_name)
            data.append(count)
        
        print(f"✅ Registration trend: {dict(zip(labels, data))}")
        
        return Response({
            'labels': labels,
            'data': data
        })
        
    except Exception as e:
        print(f"❌ Error in get_registration_trend: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'labels': ['จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.', 'อา.'],
            'data': [0, 0, 0, 0, 0, 0, 0]
        }, status=500)
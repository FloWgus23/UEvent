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


#อัปเตดสถานะกิจกรรม
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


#ใช้ Time Decay ( ทาม-ดีเค ) ในการลดคะแนนความสนใจเมื่อเปลี่ยนไปตามเวลาครับ
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


# อัพเดต implicit_score ( คะแนนที่คอยเก็บจากการที่ดูกิจกรรม - ลงทะเบียนกิจกรรม - ยกเลิกการลงทะเบียนกิจกรรม )
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
            'view': 0.5,                 #ดูกิจกรรม 
            'register': 2.5,             #ลงทะเบียนกิจกรรม 
            'unregister': -1.5           #ยกเลิกการลงทะเบียนกิจกรรม
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




#กิจกรรมทั้งหมด
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
    #กลุ่มคำสั่งพิเศษใช้ Action
    # ลงทะเบียนกิจกรรม
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

    #เช็คว่าลงทะเบียนกิจกรรมยัง จะแสดงในหน้า ActivityDetail.vue ครับ
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def check_registration(self, request, pk=None):
        """เช็คว่าลงทะเบียนหรือยัง"""
        activity = self.get_object()
        is_registered = Registration.objects.filter(
            user=request.user, 
            activity=activity
        ).exists()
        return Response({'is_registered': is_registered})

    #ยกเลิกการลงทะเบียนกิจกรรม
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
    
    #ดูรายชื่อคนลงทะเบียน ฝั่งผู้สร้างกิจกรรม 
    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        activity = self.get_object()
        registrations = Registration.objects.filter(activity=activity)
        serializer = RegistrationSerializer(registrations, many=True, context={'request': request})
        return Response(serializer.data)

    #ดึงเฉพาะกิจกรรมที่เราเป็นคนสร้าง  ฝั่งผู้สร้างกิจกรรม
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
# 👤 USER PROFILE & TAG SYSTEM : โปร์ไฟล์ และ ระบบแท็ก
# ========================================

#ดึงข้อมูลโปรไฟล์ของฉัน  แสดงชื่อและข้อมูลของผู้ใช้ หรือใช้ตรง Navbar เพื่อโชว์รูปโปรไฟล์เล็กๆ
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_profile(request):
    serializer = UserProfileSerializer(request.user, context={'request': request})  #ดูจาก Token ที่แนบมา
    return Response(serializer.data)


#แสดงใน Onboarding Modal (หน้าต่างเด้งตอนสมัครใหม่) ให้ user เลือกสิ่งที่สนใจ
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_tags(request):  #ดึงแท็กทั้งหมด
    """ดึง Tags ทั้งหมด"""
    try:
        tags = Tag.objects.filter(is_active=True).order_by('name') #เรียงตาม ก-ฮ
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


#จัดการความสนใจ
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_interests(request):
    """จัดการความสนใจของผู้ใช้"""
    if request.method == 'GET':      #คือสมัครไปแล้ว เลือกไปแล้ว ไปดึง tag ที่เลือกใน Database มาแสดง 
        interests = UserInterest.objects.filter(user=request.user)
        serializer = UserInterestSerializer(interests, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':    #คือสมัครใหม่ เลือกใหม่ = แสดงหน้า Onboarding ให้ผู้ใช้เลือก แล้วบันทึกลง Database 
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


#เช็คว่าเราเป็นผู้ใช้ใหม่ = Onboarding , ถ้ามีบัญชีแล้ว = Feed
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_has_interests(request):
    has_interests = UserInterest.objects.filter(user=request.user).exists()
    return Response({'has_interests': has_interests})


# ========================================
# 🧠 RECOMMENDATION SYSTEM (IMPROVED) : ระบบแนะนำ
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
    
    ## ดึงกิจกรรมที่ "ใหม่ล่าสุด" (-created_at) และ "คนลงทะเบียนเยอะสุด" (-registered_count) 
    # เอามาแค่ 20 อันดับแรก
    def get_popular_activities():
        """ดึงกิจกรรมยอดนิยม (ล่าสุด + คนลงทะเบียนเยอะ)"""
        return Activity.objects.filter(
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']
        ).prefetch_related('tag_list').order_by('-created_at', '-registered_count')[:20]

    try:
        # ========================================
        # CASE 1: GUEST USER : ไม่ได้ล็อกอิน
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
        # CASE 2: MEMBER WITHOUT INTERESTS : Login แล้ว แต่ยังไม่เคยเลือกความสนใจ 
        # (ระบบยังไม่รู้จักนิสัย เลยส่งกิจกรรมยอดนิยมให้ดูก่อน)
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
        # CASE 3: PERSONALIZED RECOMMENDATION : Login แล้ว และมีประวัติความสนใจแล้ว
        # (ระบบรู้จักแล้วว่าชอบอะไร -> คำนวณสูตรแนะนำแบบ Personalized)
        # ========================================
        
        # 🆕 คำนวณคะแนนพร้อม Time Decay ( ทาม - ดีเค ) --ลดความสนใจ
        interests_with_decay = []
        for interest in user_interests:
            decay_factor = calculate_time_decay_factor(interest.last_updated)
            
            # คำนวณ Total Score (Explicit 70% + Implicit 30%) * Decay 
            base_score = (0.7 * float(interest.explicit_score)) + (0.3 * float(interest.implicit_score))
            final_score = base_score * decay_factor     # สูตร: (คะแนนที่เลือกเอง 70% + คะแนนพฤติกรรม 30%) * ค่าเสื่อมตามเวลา
            
            interests_with_decay.append({
                'tag_id': interest.tag_id,
                'score': final_score,
                'decay': decay_factor
            })
        
        # เรียงตามคะแนนจากมากไปน้อย
        interests_with_decay.sort(key=lambda x: x['score'], reverse=True)
        interested_tag_ids = [item['tag_id'] for item in interests_with_decay]    #ตัวอย่างเวลาดึงข้อมูล [ 5,12,3,8,7,19]
        
        # ✅ ใช้ Prefetch เพื่อแก้ N+1 Query
        matching_activities = Activity.objects.filter(
            tag_list__id__in=interested_tag_ids,              # หากิจกรรมที่มี tag ตรงกับที่เราชอบ interest_tag_ids = [5,12,3] มาดูว่ามีกิจกรรมไหนตรงกับที่เราเลือกไว้บ้าง
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']          # เอาเฉพาะที่ยังไม่จบ
        ).prefetch_related('tag_list').distinct()  #มันคือการบอก Database ว่า "ขนข้อมูล Tag ของกิจกรรมพวกนี้มาด้วยเลยนะ ทีเดียวจบ" prefetch=ดึงแท็กมาพร้อมกัน , distinct= ลบข้อมูลซ้ำ
        
        # คำนวณคะแนนความตรงกับความสนใจ สร้าง list เปล่า เพื่อเก็บกิจกรรมพร้อมคะแนน
        activities_with_score = []
        
        for activity in matching_activities:  #วนลูปทุกกกิจกรรมที่หาเจอ
            # ✅ ใช้ค่าที่ prefetch แล้ว (ไม่มี Query เพิ่ม)
            activity_tag_ids = {tag.id for tag in activity.tag_list.all()}  #ดึงแท็ก id ของกิจกรรมนี้ กิจกรรม "วิ่งมาราธอน" มี Tags: กีฬา(5), กลางแจ้ง(12), แข่งขัน(8) = {5,12,8}
            matched_tag_ids = set(interested_tag_ids) & activity_tag_ids  #หากิจกรรมที่ตรงใจกันระหว่าง User กับ แท็ก ของกิจกรรม เช่น ตรงกัน 5 กับ 12 Intersection
            
            if not matched_tag_ids:   #ถ้าไม่มีแท็กตรงกันเลย ให้ข้ามไปรอบถัดไปครับ 
                continue
            
            # รวมคะแนนจาก Tags ที่ตรงกัน
            total_score = 0
            for tid in matched_tag_ids:    #วนลูปทุก Tag ID ที่ตรงกัน  เช่น matched_tag_ids = {5,12} ----> วน 2 รอบ
                # หาคะแนนจาก interests_with_decay
                for item in interests_with_decay:    #วนลูปหาคะแนนของแท็กนี้จาก interests_with_decay
                    if item['tag_id'] == tid:      #ถ้าเจอ Tag ID ที่ตรงกัน เพิ่มคะแนนเข้า Total_score , break หยุดเมื่อเจอแล้ว
                        total_score += item['score']
                        break
            
            # Normalize score (0-1)
            max_possible = len(matched_tag_ids) * 10  # แต่ละ tag สูงสุด 10 คะแนน   จำนวนแท็กที่ตรง * 10 เช่น ตรงกัน 2 ก็เท่ากับ 2 * 10 = 20
            match_score = (total_score / max_possible) if max_possible > 0 else 0    #เพื่อให้คะแนนอยู่ในช่วง 0 - 1 , ป้องกันการหารด้วย 0
            #การหารด้วย max_possible เพื่อปรับคะแนนให้อยู่ในช่วง 0 ถึง 1 เสมอ ทำให้เปรียบเทียบง่ายครับ

            #  max_possible = 2 * 10 = 20
            #  match_score = 12.18/20 = 0.609 (60.9%)
            
            activities_with_score.append({   #เพิ่ม dic เข้า list
                'activity': activity,    #object ของกิจกรรม 
                'match_score': round(match_score, 2),   #คะแนนความตรงกัน ปัดเศษ 2 ตำแหน่ง
                'matched_tags': len(matched_tag_ids)   #จำนวนแท็กที่ตรง
            })

            # activities_with_score = [
            #   {
            #      'activity':<Activity: วิ่งมาราธอน >,
            #      'match_score':0.85,
            #      'matched_tags':3
            #    }
            #]
        
        # ========================================
        # FALLBACK: ถ้าไม่เจอกิจกรรมที่ตรงใจ : ถ้าหาที่ตรงใจไม่ได้เลย สักอันเดียว" (เช่น ผู้ใช้ชอบ Tag แปลกๆ ที่ช่วงนี้ไม่มีกิจกรรมจัดเลย)
        # ระบบจะไม่ส่งหน้าว่างๆ กลับไป แต่จะเปลี่ยนแผนไปดึง "กิจกรรมยอดฮิต" (Popular) มาแสดงแทนครับ ให้ User มีอะไรดูแก้ขัดไปก่อน
        # ========================================
        if not activities_with_score:   #เช็คว่า activities_with_score ว่างมั้ย
            activities = get_popular_activities()  #เรียกใช้ get_popular_activities
            serializer = ActivitySerializer(activities, many=True, context={'request': request})
            return Response({
                'activities': serializer.data,
                'recommendation_type': 'popular_fallback',
                'has_interests': True,
                'message': 'ไม่พบกิจกรรมที่ตรงกับความสนใจ (แสดงกิจกรรมล่าสุดแทน)'
            })

        # ========================================
        # 🆕 DIVERSITY: 80% Personalized + 20% Random 
        # เลือกกิจกรรมที่คะแนนเยอะที่สุดมา 80%
        # ไปสุ่มกิจกรรมอื่นที่ ไม่ได้อยู่ใน list ข้างบน มาอีก 20%
        # ========================================
        
        # เรียงลำดับกิจกรรมตามคะแนน   กำหนดเกณฑ์การเรียง  คะแนนสูงสุดก่อน ถ้าคะแนนเท่ากัน ให้ดู Tags ที่ตรงเยอะกว่า
        activities_with_score.sort(key=lambda x: (-x['match_score'], -x['matched_tags'])) 
        
        # แบ่งเป็น 80% Personalized
        personalized_count = max(1, int(len(activities_with_score) * 0.8))  #คำนวณจากกิจกรรมที่จะเลือก = 80% ของทั้งหมด , int ปัดเศษลง , ป้องกันการเป็น 0   1 รายการ
        # สมมุติมี 10 รายการ personalized_count = int(10*0.8) = 8 รายการ
        # สมมุติมี 3 รายการ personalized_count = int(3*0.8) = 2 รายการ ไม่ใช้ 2.4 
        # สมมุติมี 1 รายการ personalized_count = int(1*0.8) = 0 , max(1,0) = 1 รายการ <---- ป้องกันเป็น 0


        personalized_activities = activities_with_score[:personalized_count] # ตัด list เอาเฉพาะ 80 % แรก ได้กิจกรรมที่มีคะแนนสูงสุด
        #ตัวอย่างมี 10 รายการเลือกมา 8 รายการ
        
        # เพิ่ม 20% Random (สำหรับ Exploration)
        used_activity_ids = {item['activity'].id for item in personalized_activities} #สร้าง set ของ id กิจกรรมที่เลือกไปแล้ว (80%), กันไว้ไม่ให้ซ้ำ
         #used_activity_ids = {1,3,4,5,7,9,14,19} 


        #เพื่อแก้ปัญหา Filter Bubble (การเห็นแต่สิ่งเดิมๆ) เผื่อ User จะเจอความสนใจใหม่ๆ ที่ไม่เคยรู้ตัวมาก่อน
        #ดึงกิจกรรมแบบสุ่ม 5 รายการ 
        random_activities = Activity.objects.filter(
            status__in=['กำลังรับสมัคร', 'กำลังดำเนินการ']    #เอาเฉพาะที่ยังเปิดรับสมัคร
        ).exclude(
            id__in=used_activity_ids               #ไม่เอาที่ซ้ำกับ 80% ที่เลือกแล้ว 
        ).prefetch_related('tag_list').order_by('?')[:5]  # สุ่ม 5 กิจกรรม 
                                     #เรียงแบบสุ่ม

        # รวมกัน
        for activity in random_activities:   #เพิ่มกิจกรรมสุ่มเข้า list
            activities_with_score.append({
                'activity': activity,
                'match_score': 0.0,             #ตั้งคะแนนเป็น 0.0 เพราะไม่ได้คำนวน
                'matched_tags': 0               #ตั้ง matched_tags เป็น 0 (เพราะไม่ได้ตรงตามความสนใจ)
            })
        
       #ขั้นตอนนี้จะได้ 13 กิจกรรมแล้ว ได้จาก 80% มา 8 กิจกรรม + สุ่มอีก 5 กิจกรรม รวมเป็น 13

        # Shuffle เล็กน้อย (เว้น Top 3)  
        top_3 = personalized_activities[:3]           # เก็บ 3 อันดับแรกไว้    ต้องอยู่บนสุดเสมอ
        rest = personalized_activities[3:] + [        # เอาที่เหลือ + ของสุ่ม มารวมกัน   อันดับ 4 เป็นต้นไปคือ 80% ที่เหลือ
            {'activity': act, 'match_score': 0.0, 'matched_tags': 0}     #กิจกรรมสุ่ม 5 รายการแปลงเป็น Dic Format
            for act in random_activities
        ]
        #personalized_activities = 8 รายการ
        #top_3 = [อันดับ 1,2,3]
        #rest = [อันดับ 4,5,6,7] + [สุ่ม 1,2,3,4,5]
        #rest = 10 รายการ

        random.shuffle(rest)                         # เขย่ารวมกัน (Shuffle)
        #สุ่มเรียงลำดับ rest  ทำให้ได้กิจกรรมแบบสุ่ม
        #ก่อน shuffle = [อันดับ 4,5,6,7 สุ่ม 1,2,3,4,5]
        #หลัง shuffle = [สุ่ม2, อันดับ5, สุ่ม4, อันดับ7, สุ่ม1, อันดับ4, .....]
        
        final_list = top_3 + rest                           #รวม top 3 กับ rest ที่ shuffle แล้ว
        final_list = final_list[:20]  # จำกัดแค่ 20 กิจกรรม
        
        # ========================================
        # SERIALIZE RESULT
        # ========================================
        result = []         #สร้าง list เปล่า เพื่อเก็บผลลัพธ์สุดท้าย
        for item in final_list:       #วนลูกทุกกิจกรรมใน final_list 20 รายการ
            data = ActivitySerializer(item['activity'], context={'request': request}).data     #แปลง Obj เป็น JSON , .data คือดึงข้อมูลออกมา
            #เพิ่ม 2 filed เข้าไปใน JSON 
            data['match_score'] = item['match_score']   #คะแนนความตรงกัน
            data['matched_tags'] = item['matched_tags']   #จำนวน Tag ที่ตรง 
            #Frontend สามารถแสดงเป็น ตรงใจ 85% หรือ Badge ได้
            result.append(data)   #เพิ่ม dic เข้า list result

        #result = [
        #   {
        #    'id': 123,
        #    'name': 'วิ่งมาราธอน',
        #    'description': " ",
        #    'match_score': 0.85,  ---->  เพิ่มเข้ามาใหม่
        #    'matched_tags': 3    ---->  เพิ่มเข้ามาใหม่
        #    ......
        #    }
        
        return Response({
            'activities': result,   #ส่งข้อมูลกิจกรรม พร้อมคะแนน
            'recommendation_type': 'personalized',    #บอกประเภทการแนะนำ Fromtend = เป็นการแนะนำสำหรับคุณ
            'has_interests': True,     # บอกว่า user มีความสนใจแล้ว
            'message': None,
            'debug_info': {   #เพิ่มการ Debug 
                'total_interests': len(user_interests),   #จำนวนความสนใจทั้งหมด
                'personalized_count': len(personalized_activities),   #จำนวนกิจกรรมแนะนำ 80%
                'random_count': len(random_activities),  #จำนวนกิจกรรมแบบสุ่ม 20%
                'top_tags': [item['tag_id'] for item in interests_with_decay[:5]]  # Top 5 แท็ก ที่สนใจมากที่สุด
            }
        })
        
    except Exception as e:   #จับ error ทุกประเภท ถ้ามี
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
# 📊 ORGANIZER DASHBOARD STATISTICS : หน้าแดชบอร์ดฝั่งผู้สร้างกิจกรรม
# ========================================

#แสดงสัดส่วนและรายละเอียดของแดชบอร์ดต่างๆครับ
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


#แสดงแนวโน้มการลงทะเบียนของฝั่งผู้จัดกิจกรรม
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
    


# -------------------------------------------------------------------------
# View Functions (Inline definition)
# -------------------------------------------------------------------------

#แสดงกิจกรรมทั้งหมดที่ user ลงทะเบียนกิจกรรม - หน้ากิจกรรมของฉัน
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_registrations(request):
    """ดึงการลงทะเบียนทั้งหมดของ User"""
    registrations = Registration.objects.filter(
        user=request.user
    ).select_related('activity').order_by('-registered_at')
    
    serializer = RegistrationSerializer(
        registrations, 
        many=True, 
        context={'request': request}
    )
    return Response(serializer.data)


#ยกเลิกการลงทะเบียน
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_registration(request, registration_id):
    """ยกเลิกการลงทะเบียน"""
    try:
        registration = Registration.objects.get(
            id=registration_id, 
            user=request.user
        )
        activity = registration.activity
        # คืนจำนวนคนลงทะเบียน
        activity.registered_count = max(0, activity.registered_count - 1)
        activity.save()
        
        registration.delete()
        
        return Response({
            'message': 'ยกเลิกการลงทะเบียนสำเร็จ'
        }, status=200)
        
    except Registration.DoesNotExist:
        return Response({
            'message': 'ไม่พบข้อมูลการลงทะเบียน'
        }, status=404)
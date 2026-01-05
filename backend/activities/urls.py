# backend/activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# ⭐ เพิ่มส่วนนี้สำหรับ JWT Authentication (Login)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ActivityViewSet,
    get_current_user_profile,
    # Tag System Views
    get_all_tags,
    user_interests,
    check_user_has_interests,
    recommended_activities
)
from .models import Registration
from .serializers import RegistrationSerializer

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')

# -------------------------------------------------------------------------
# View Functions (Inline definition)
# -------------------------------------------------------------------------

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

# -------------------------------------------------------------------------
# URL Patterns
# -------------------------------------------------------------------------

urlpatterns = [
    # ========================================
    # 🔐 AUTHENTICATION (สำคัญ! ต้องมีส่วนนี้)
    # ========================================
    # สำหรับ Login เอา Token (ใช้ใน Postman และ Frontend)
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_alias'), # Alias สำหรับคนชิน path นี้
    
    # สำหรับต่ออายุ Token (Refresh)
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ========================================
    # 📝 REGISTRATION URLS
    # ========================================
    path('my-registrations/', my_registrations, name='my-registrations'),
    path('registrations/<int:registration_id>/cancel/', cancel_registration, name='cancel-registration'),
    
    # ========================================
    # 👤 USER PROFILE
    # ========================================
    path('user/profile/', get_current_user_profile, name='user-profile'),
    
    # ========================================
    # 🏷️ TAG SYSTEM & RECOMMENDATION URLs
    # ========================================
    
    # Tags
    path('tags/', get_all_tags, name='tags-list'),
    
    # User Interests
    path('user/interests/', user_interests, name='user-interests'),
    path('user/has-interests/', check_user_has_interests, name='check-interests'),
    
    # ⭐ Recommendations
    path('activities/recommended/', recommended_activities, name='recommended-activities'),
    
    # ========================================
    # 🔗 MAIN ROUTER (ต้องมาทีหลังสุด!)
    # ========================================
    path('', include(router.urls)),
]
# backend/activities/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# เพิ่มส่วนนี้สำหรับ JWT Authentication (Login)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    ActivityViewSet,
    get_current_user_profile,
    get_all_tags,
    user_interests,
    check_user_has_interests,
    recommended_activities,
    get_faculty_statistics,
    get_registration_trend,
    my_registrations,       
    cancel_registration,    
)
from .models import Registration
from .serializers import RegistrationSerializer

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')


urlpatterns = [
   
    #สำหรับ Login เอา Token (ใช้ใน Postman และ Frontend)
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_alias'), # Alias สำหรับคนชิน path นี้
    
    #สำหรับต่ออายุ Token (Refresh)
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #สำหรับการลงทะเบียน
    path('my-registrations/', my_registrations, name='my-registrations'),
    path('registrations/<int:registration_id>/cancel/', cancel_registration, name='cancel-registration'),
    
    #สำหรับโปรไฟล์
    path('user/profile/', get_current_user_profile, name='user-profile'),

    path('statistics/faculty/', get_faculty_statistics, name='faculty-statistics'),
    path('statistics/registration-trend/', get_registration_trend, name='registration-trend'),
    
    # ระบบแท็ก : แท็ก , ความสนใจของผู้ใช้ , การแนะนำ
    # Tags : แท็ก
    path('tags/', get_all_tags, name='tags-list'),
    
    # User Interests : ความสนใจ
    path('user/interests/', user_interests, name='user-interests'),
    path('user/has-interests/', check_user_has_interests, name='check-interests'),
    
    # Recommendations : การแนะนำ
    path('activities/recommended/', recommended_activities, name='recommended-activities'),
    
    path('', include(router.urls)),
]
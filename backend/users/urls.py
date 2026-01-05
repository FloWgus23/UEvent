# backend/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    UserProfileView,
    upload_profile_image,
    delete_profile_image,
    request_organizer_role # ⭐
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/upload-image/', upload_profile_image, name='upload-profile-image'),
    path('me/delete-image/', delete_profile_image, name='delete-profile-image'),
    
    # ⭐ Path สำหรับขอสิทธิ์
    path('request-organizer/', request_organizer_role, name='request-organizer'),
]
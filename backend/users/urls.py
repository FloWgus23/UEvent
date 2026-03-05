# backend/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    UserProfileView,
    upload_profile_image,
    delete_profile_image,
    request_organizer_role 
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),         # ลงทะเบียนสมาชิกใหม่
    path('login/', TokenObtainPairView.as_view(), name='login'),        # ล็อกอิน: ส่ง User/Pass มา แลกเป็น Token (กุญแจเข้าบ้าน)
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),       # จุดต่ออายุ: เอา Refresh Token มาแลก Access Token ใหม่ (ไม่ต้องล็อกอินซ้ำ)
    
    path('me/', UserProfileView.as_view(), name='user-profile'),           # ดูข้อมูลส่วนตัว หรือแก้ไขชื่อ/เบอร์โทร
    
    path('me/upload-image/', upload_profile_image, name='upload-profile-image'),     # อัปโหลดรูปโปรไฟล์ใหม่
    path('me/delete-image/', delete_profile_image, name='delete-profile-image'),     # ลบรูปโปรไฟล์ทิ้ง (กลับไปใช้รูปเดิม)

    path('request-organizer/', request_organizer_role, name='request-organizer'),     #ส่งเอกสารขอเลื่อนขั้นเป็น "ผู้จัดกิจกรรม"
]
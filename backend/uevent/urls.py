# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('activities.urls')),    #กิจกรรม
     # เพิ่มบรรทัดนี้ครับ เพื่อให้ Vue ยิงมาที่ /api/auth/password_reset/ ได้
    path('api/auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/auth/', include('users.urls')),    #ผู้ใช้
    path('api/', include('news.urls')),          #ข่าว
    # ⭐ เพิ่มบรรทัดนี้ครับ!
    path('api/notifications/', include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('activities.urls')),    #กิจกรรม
    path('api/auth/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),  #รีเซ็ตรหัสผ่าน
    path('api/auth/', include('users.urls')),    #ผู้ใช้
    path('api/', include('news.urls')),          #ข่าว
    path('api/notifications/', include('notifications.urls')),  #แจ้งเตือน
]

# Serve media files in development
##if settings.DEBUG:
 ##   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

##if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from rest_framework import serializers
from .models import Notification

#ตัวแปลงข้อมูลที่สร้างมาจาก Model โดยตรง (ไม่ต้องเขียนโค้ดเองเยอะ มันจะไปดูโครงสร้างจาก models.py ให้เอง
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'is_read', 'created_at']
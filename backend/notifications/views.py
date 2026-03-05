# backend/notifications/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

## ตัวจัดการระบบแจ้งเตือน
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    # "ต้องล็อกอินก่อน" ถึงจะใช้งานได้
    permission_classes = [IsAuthenticated]
    # ⭐ แก้ไขตรงนี้: เพิ่ม 'post' เข้าไปในรายการ
    http_method_names = ['get', 'post', 'patch', 'delete'] 
    
    # ดูได้เฉพาะ "ของใครของมัน" (ห้ามเห็นของคนอื่น)
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    # เอาไว้นับว่ามีกี่อันที่ "ยังไม่ได้อ่าน" (ส่งตัวเลขไปโชว์ที่กระดิ่ง)
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """นับจำนวนที่ยังไม่อ่าน"""
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'count': count})
    
    
    # เมื่อ user จิ้มที่แจ้งเตือนอันไหน ก็เปลี่ยนสถานะเป็น "อ่านแล้ว"
    @action(detail=True, methods=['post'], url_path='read')
    def mark_read(self, request, pk=None):
        """บันทึกว่าอ่านแจ้งเตือนนี้แล้ว"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Marked as read'})

    # ปุ่ม "อ่านทั้งหมด" กดทีเดียว ทุกอันกลายเป็นอ่านแล้วทันที
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """อ่านทั้งหมด"""
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({'message': 'All marked as read'})
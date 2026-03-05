# news/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import News
from .serializers import NewsSerializer

#จัดการ CRUD (Create, Read, Update, Delete) ให้เองอัตโนมัติ
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer

    #Create: สร้างข่าวใหม่
    # ⭐ บันทึก owner เมื่อสร้างข่าวใหม่
    def perform_create(self, serializer):
        status = self.request.data.get('status', 'draft')
        serializer.save(status=status, owner=self.request.user)

    #Update: ปรับแต่งตอนแก้ไขข่าว
    def perform_update(self, serializer):
        status = self.request.data.get('status', serializer.instance.status)
        serializer.save(status=status)
    
    # ⭐ เพิ่ม Custom Action: ดึงข่าวที่ตัวเองสร้าง สำหรับหน้า ผู้สร้างกิจกรรม
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_news(self, request):
        """
        ดึงเฉพาะข่าวที่ User ปัจจุบันเป็นคนสร้าง
        สำหรับหน้า Organizer Dashboard
        """
        news = News.objects.filter(owner=request.user).order_by('-created_at')
        serializer = NewsSerializer(news, many=True, context={'request': request})
        return Response(serializer.data)
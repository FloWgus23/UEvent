# backend/users/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer
from .models import UserProfile

#การลงทะเบียน รับข้อมูลสมัครสมาชิก (Username, Password, Email)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

#จัดการโปรไฟล์
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):   #get (ดูข้อมูล): ดึงข้อมูลของ "ฉัน" (User ที่ Login อยู่) ออกมาดู
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request):    #(แก้ไขทั้งหมด): แก้ไขข้อมูลแบบยกชุด
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            user_serializer = UserSerializer(request.user, context={'request': request})
            return Response({
                'message': 'อัปเดตข้อมูลสำเร็จ',
                'data': user_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):    #(แก้ไขบางส่วน): แก้ไขแค่บางฟิลด์ เช่น อยากแก้แค่เบอร์โทร ก็ส่งมาแค่เบอร์โทร (Field อื่นค่าเดิมไม่หาย)
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user_serializer = UserSerializer(request.user, context={'request': request})
            return Response({
                'message': 'อัปเดตข้อมูลสำเร็จ',
                'data': user_serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#จัดการรูปโปรไฟล์
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_profile_image(request):      #เช็คว่ามีไฟล์ส่งมาไหม ถ้า User มีรูปเดิมอยู่แล้ว ระบบจะลบทิ้งก่อน (เพื่อไม่ให้เปลืองพื้นที่ Server) แล้วค่อยเซฟรูปใหม่
    if 'profile_image' not in request.FILES:
        return Response({'error': 'กรุณาเลือกรูปภาพ'}, status=status.HTTP_400_BAD_REQUEST)
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if profile.profile_image:
        profile.profile_image.delete(save=False)
    
    profile.profile_image = request.FILES['profile_image']
    profile.save()
    
    user_serializer = UserSerializer(request.user, context={'request': request})
    return Response({
        'message': 'อัปโหลดรูปโปรไฟล์สำเร็จ',
        'data': user_serializer.data
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_image(request):          #สั่งลบรูปโปรไฟล์ทิ้ง ให้กลับไปใช้รูป Default
    if hasattr(request.user, 'profile') and request.user.profile.profile_image:
        request.user.profile.profile_image.delete(save=True)
        user_serializer = UserSerializer(request.user, context={'request': request})
        return Response({
            'message': 'ลบรูปโปรไฟล์สำเร็จ',
            'data': user_serializer.data
        })
    return Response({'error': 'ไม่มีรูปโปรไฟล์ให้ลบ'}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def request_organizer_role(request):     #ขอสิทธิ์เป็นผู้จัดกิจกรรม
#     """User กดส่งคำขอเป็นผู้จัด"""
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     #เช็คสถานะก่อน:
#     if profile.organizer_status == 'pending':
#         return Response({'message': 'คำขอของคุณอยู่ระหว่างการพิจารณา'}, status=status.HTTP_400_BAD_REQUEST)
    
#     if profile.organizer_status == 'approved':
#         return Response({'message': 'คุณเป็นผู้จัดกิจกรรมอยู่แล้ว'}, status=status.HTTP_400_BAD_REQUEST)
    
#     profile.organizer_status = 'pending'
#     profile.save()
    
#     # ส่งข้อมูลกลับไปอัปเดตหน้าจอทันที
#     user_serializer = UserSerializer(request.user, context={'request': request})
#     return Response({
#         'message': 'ส่งคำขอเรียบร้อยแล้ว กรุณารอการอนุมัติจากผู้ดูแลระบบ',
#         'data': user_serializer.data
#     })

# API ใหม่: ขอสิทธิ์เป็นผู้จัดกิจกรรม
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser]) # ⭐ รองรับ FormData
def request_organizer_role(request):
    """User ส่งคำขอพร้อมเอกสาร"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # 1. เช็คสถานะปัจจุบัน
    if profile.organizer_status == 'pending':
        return Response({'message': 'คำขอของคุณอยู่ระหว่างการพิจารณาแล้ว'}, status=status.HTTP_400_BAD_REQUEST)
    
    if profile.organizer_status == 'approved':
        return Response({'message': 'คุณเป็นผู้จัดกิจกรรมอยู่แล้ว'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. รับไฟล์เอกสาร (key: 'document')
    if 'document' in request.FILES:
        file = request.FILES['document']
        
        # Validation: เช็คขนาดไฟล์ (5MB)
        if file.size > 5 * 1024 * 1024:
             return Response({'message': 'ขนาดไฟล์ต้องไม่เกิน 5MB'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validation: เช็คประเภทไฟล์
        allowed_types = ['image/jpeg', 'image/png', 'application/pdf']
        if file.content_type not in allowed_types:
             return Response({'message': 'รองรับเฉพาะไฟล์รูปภาพ (JPG, PNG) และ PDF เท่านั้น'}, status=status.HTTP_400_BAD_REQUEST)

        profile.verification_doc = file
    else:
        # บังคับว่าต้องมีไฟล์
        return Response({'message': 'กรุณาแนบเอกสารยืนยันตัวตน'}, status=status.HTTP_400_BAD_REQUEST)

    # 3. บันทึก
    profile.organizer_status = 'pending'
    profile.save()
    
    user_serializer = UserSerializer(request.user, context={'request': request})
    return Response({
        'message': 'ส่งคำขอและเอกสารเรียบร้อยแล้ว กรุณารอการตรวจสอบ',
        'data': user_serializer.data
    })
    
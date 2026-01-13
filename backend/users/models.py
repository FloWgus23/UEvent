# backend/users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ORGANIZER_STATUS_CHOICES = [
        ('none', 'ทั่วไป'),
        ('pending', 'รออนุมัติ'),
        ('approved', 'ผู้จัดกิจกรรม'),
        ('rejected', 'ไม่อนุมัติ'),
    ]

    # ⭐ เพิ่มตัวเลือกสำหรับ Dropdown
    GENDER_CHOICES = [
        ('male', 'ชาย'),
        ('female', 'หญิง'),
        ('other', 'อื่นๆ'),
    ]

    FACULTY_CHOICES = [
        ('science', 'คณะวิทยาศาสตร์'),
        ('engineering', 'คณะวิศวกรรมศาสตร์'),
        ('business', 'คณะบริหารศาสตร์'),
        ('liberal_arts', 'คณะศิลปศาสตร์'),
        ('agriculture', 'คณะเกษตรศาสตร์'),
        ('nursing', 'คณะพยาบาลศาสตร์'),
        ('pharmacy', 'คณะเภสัชศาสตร์'),
        ('law', 'คณะนิติศาสตร์'),
        ('political', 'คณะรัฐศาสตร์'),
        ('other', 'อื่นๆ'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='รูปโปรไฟล์')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='เบอร์โทรศัพท์')
    bio = models.TextField(blank=True, null=True, verbose_name='ประวัติส่วนตัว')
    
    # ⭐ Field ใหม่ที่เพิ่มเข้ามา
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='เพศ')
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, blank=True, null=True, verbose_name='คณะ')
    birthdate = models.DateField(blank=True, null=True, verbose_name='วันเกิด')

    organizer_status = models.CharField(
        max_length=20, 
        choices=ORGANIZER_STATUS_CHOICES, 
        default='none',
        verbose_name='สถานะผู้จัด'
    )

    verification_doc = models.FileField(
        upload_to='verification_docs/', 
        blank=True, 
        null=True, 
        verbose_name='เอกสารยืนยันตัวตน'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'โปรไฟล์ผู้ใช้'
        verbose_name_plural = 'โปรไฟล์ผู้ใช้'
    
    def __str__(self):
        return f"{self.user.username} ({self.get_organizer_status_display()})"

# ... (Signals คงเดิม) ...
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
   
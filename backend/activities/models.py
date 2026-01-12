# backend/activities/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# ========================================
# 🆕 TAG SYSTEM MODELS
# ========================================
# เก็บ tag กลางทั้งหมด 
class Tag(models.Model):
    """
    Tags สำหรับระบบ Recommendation
    เช่น IT, Music, Sport, Art, Workshop, etc.
    """
    name = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name="ชื่อแท็ก"
    )
    
    icon = models.TextField(
        blank=True,
        null=True,
        help_text="Emoji หรือ icon (เช่น 💻, 🎵)",
        verbose_name="ไอคอน"
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="คำอธิบาย"
    )
    
    color = models.CharField(
        max_length=7,
        default="#3B82F6",
        help_text="สีแบบ HEX (เช่น #3B82F6)",
        verbose_name="สี"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="ใช้งานอยู่"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tag'
        ordering = ['name']
        verbose_name = 'แท็ก'
        verbose_name_plural = 'แท็ก'
    
    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name

#ความสนใจของผู้ใช้งาน 
class UserInterest(models.Model):
    """
    ความสนใจของผู้ใช้แต่ละคน
    เก็บทั้ง Explicit (เลือกเอง) และ Implicit (จากพฤติกรรม)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interests',
        verbose_name="ผู้ใช้"
    )
    
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='user_interests',
        verbose_name="แท็ก"
    )
    
    #คะแนนที่เลือกเองตอนสมัครใหม่
    explicit_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        help_text="คะแนนจากการเลือก (0-10)",
        verbose_name="คะแนนแบบตรง"
    )
    
    #คะแนนที่แอบเก็บความสนใจ เช่น การดูกิจกรรม ลงทะเบียน และยกเลิกกิจกรรม
    implicit_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="คะแนนจากพฤติกรรม",
        verbose_name="คะแนนจากพฤติกรรม"
    )
    
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_interest'
        unique_together = ('user', 'tag')
        ordering = ['-explicit_score', '-implicit_score']
        verbose_name = 'ความสนใจของผู้ใช้'
        verbose_name_plural = 'ความสนใจของผู้ใช้'
    
    def __str__(self):
        return f"{self.user.username} - {self.tag.name} (E:{self.explicit_score}, I:{self.implicit_score})"
    
    @property
    def total_score(self): #สูตรที่ใช้คำนวณคะแนนรวมครับ
        """คำนวณคะแนนรวม (70% explicit + 30% implicit)"""
        return (0.7 * float(self.explicit_score)) + (0.3 * float(self.implicit_score))

#กิจกรรมกับการเลือก tag ได้แบบ Many-to-many
class ActivityTag(models.Model):
    """
    Many-to-Many ระหว่าง Activity กับ Tag
    """
    activity = models.ForeignKey(
        'Activity',
        on_delete=models.CASCADE,
        related_name='activity_tags'
    )
    
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='activity_tags'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity_tag'
        unique_together = ('activity', 'tag')    # ป้องกันการแปะ Tag เดิมซ้ำในกิจกรรมเดียว
        verbose_name = 'แท็กของกิจกรรม'
        verbose_name_plural = 'แท็กของกิจกรรม'
    
    def __str__(self):
        return f"{self.activity.name} - {self.tag.name}"


# ========================================
# EXISTING MODELS
# ========================================

#กิจกรรมทั้งหมด รายละเอียดกิจกรรม ใครเป็นคนสร้าง, จัดที่ไหน, เมื่อไหร่, รับกี่คน
class Activity(models.Model):   
    # สถานะของกิจกรรม
    STATUS_CHOICES = [
        ('กำลังรับสมัคร', 'กำลังรับสมัคร'),
        ('กำลังดำเนินการ', 'กำลังดำเนินการ'),
        ('สิ้นสุดแล้ว', 'สิ้นสุดแล้ว'),
    ]
    
    # หมวดหมู่มาตรฐาน
    CATEGORY_CHOICES = [
        ('academic', 'วิชาการและการเรียนรู้'),
        ('technology', 'เทคโนโลยีและนวัตกรรม'),
        ('entertainment', 'บันเทิงและนันทนาการ'),
        ('sports', 'กีฬาและสุขภาพ'),
        ('volunteer', 'จิตอาสาและสังคม'),
        ('career', 'แนะแนวและอาชีพ'),
        ('other', 'อื่นๆ'),
    ]
    
    # ⭐ เพิ่มฟิลด์ owner
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_activities',
        verbose_name='ผู้สร้าง',
        null=True,  # เพื่อให้ migrate ได้ (กิจกรรมเก่าที่ยังไม่มี owner)
        blank=True
    )
    
    name = models.CharField(max_length=255, verbose_name='ชื่อกิจกรรม')
    description = models.TextField(verbose_name='รายละเอียด')
    date = models.DateField(verbose_name='วันที่จัด')
    start_time = models.TimeField(verbose_name='เวลาเริ่มต้น', null=True, blank=True)
    end_time = models.TimeField(verbose_name='เวลาสิ้นสุด', null=True, blank=True)
    capacity = models.IntegerField(verbose_name='จำนวนรับ')
    location = models.CharField(max_length=255, verbose_name='สถานที่')
    organizer = models.CharField(max_length=255, verbose_name='หน่วยงานจัด')
    
    # เก็บ tags แบบเก่าไว้ (backward compatibility)
    tags = models.CharField(max_length=255, blank=True, null=True, verbose_name='แท็ก (เก่า)')
    
    # Many-to-Many กับ Tag ใหม่
    tag_list = models.ManyToManyField(
        Tag,
        through='ActivityTag',
        related_name='activities',
        verbose_name='แท็ก',
        blank=True
    )
    
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='other', 
        verbose_name='หมวดหมู่'
    )
    
    image = models.ImageField(upload_to='activities/', blank=True, null=True, verbose_name='รูปภาพ')
    registered_count = models.IntegerField(default=0, verbose_name='จำนวนผู้ลงทะเบียน')
    
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='กำลังรับสมัคร',
        verbose_name='สถานะ'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='วันที่สร้าง')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='วันที่แก้ไข')
    
    class Meta:
        verbose_name = 'กิจกรรม'
        verbose_name_plural = 'กิจกรรม'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def registration_status(self):
        """แสดงสถานะการลงทะเบียน"""
        return f"{self.registered_count}/{self.capacity}"
    
    @property
    def time_display(self):
        """แสดงช่วงเวลา"""
        if self.start_time and self.end_time:
            return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        return None

#เก็บการลงทะเบียนของ User คนไหน -> สมัครกิจกรรมอะไร -> เมื่อไหร่
class Registration(models.Model):
    """การลงทะเบียนกิจกรรม"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='registrations', 
        verbose_name='ผู้ลงทะเบียน'
    )
    activity = models.ForeignKey(
        Activity, 
        on_delete=models.CASCADE, 
        related_name='registrations', 
        verbose_name='กิจกรรม'
    )
    
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='เบอร์โทรศัพท์')
    note = models.TextField(blank=True, null=True, verbose_name='หมายเหตุ')
    
    status = models.CharField(max_length=20, default='registered', verbose_name='สถานะ')
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='วันที่ลงทะเบียน')

    class Meta:
        unique_together = ('user', 'activity')
        verbose_name = 'การลงทะเบียน'
        verbose_name_plural = 'การลงทะเบียน'
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} -> {self.activity.name}"
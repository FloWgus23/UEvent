# news/models.py
from django.db import models
from django.contrib.auth.models import User

#สถานะข่าว
status_choices = (
    ('draft', 'ฉบับร่าง'),
    ('published', 'เผยแพร่แล้ว'),
)

class News(models.Model):
    # ⭐ เพิ่มฟิลด์ owner   เจ้าของข่าว
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,            # ถ้า User โดนลบ ข่าวก็หายไปด้วย
        related_name='owned_news',           # เอาไว้เรียกย้อนกลับ user.owned_news.all()
        verbose_name='ผู้สร้าง',        
        null=True,  # เพื่อให้ migrate ได้
        blank=True
    )
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='draft')  # ⭐ เพิ่มฟิลด์นี้
    created_at = models.DateTimeField(auto_now_add=True)      #บันทึกเวลาที่กดสร้างข่าว ให้อัตโนมัติ

    def __str__(self):
        return self.title
# news/models.py
from django.db import models
from django.contrib.auth.models import User

status_choices = (
    ('draft', 'ฉบับร่าง'),
    ('published', 'เผยแพร่แล้ว'),
)

class News(models.Model):
    # ⭐ เพิ่มฟิลด์ owner
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_news',
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
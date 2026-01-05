from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    RECIPIENT_CHOICES = [
        ('all', 'ทุกคน'),
        ('user', 'รายบุคคล')
    ]
    
    TYPE_CHOICES = [
        ('info', 'ข่าวสาร'),
        ('success', 'สำเร็จ'),
        ('warning', 'แจ้งเตือน'),
        ('error', 'ข้อผิดพลาด')
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='หัวข้อ')
    message = models.TextField(verbose_name='ข้อความ')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False, verbose_name='อ่านแล้ว')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'การแจ้งเตือน'
        verbose_name_plural = 'การแจ้งเตือน'

    def __str__(self):
        return f"{self.title} - {self.recipient.username if self.recipient else 'All'}"
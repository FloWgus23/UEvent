import uuid
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Popup(models.Model):
    title = models.CharField("หัวข้อ", max_length=120)
    message = models.TextField("ข้อความ", blank=True)
    image = models.ImageField("รูป", upload_to="popups/", blank=True, null=True)  # ตั้งให้เหมือน Activity
    link_url = models.CharField("ลิงก์เมื่อคลิกรูป", max_length=500, blank=True)

    duration_days = models.PositiveIntegerField(
        "แสดงกี่วัน", default=7,
        validators=[MinValueValidator(1), MaxValueValidator(365)],
    )
    start_at = models.DateTimeField(
        "เริ่มแสดง", null=True, blank=True,
        help_text="เว้นว่าง = นับจากตอนกดเผยแพร่",
    )
    delay_seconds = models.PositiveIntegerField(                # เพิ่มใหม่
        "หน่วงก่อนแสดง (วินาที)", default=3,
        validators=[MaxValueValidator(60)],
        help_text="รอหลังผู้ใช้เข้าหน้าเว็บกี่วินาที แล้วค่อยแสดง popup",
    )
    auto_close_seconds = models.PositiveIntegerField(
        "จางหายเองหลังกี่วินาที", default=10,
        validators=[MaxValueValidator(120)],
        help_text="0 = ไม่จางหายเอง",
    )

    is_published = models.BooleanField("เผยแพร่", default=False)
    published_at = models.DateTimeField(null=True, blank=True, editable=False)
    end_at = models.DateTimeField(null=True, blank=True, editable=False)  # คำนวณให้อัตโนมัติ

    preview_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        was_published = bool(self.pk) and Popup.objects.filter(
            pk=self.pk, is_published=True
        ).exists()
        if self.is_published and not was_published:
            self.published_at = timezone.now()          # เริ่มนับวันใหม่ทุกครั้งที่กดเผยแพร่
        base = self.start_at or self.published_at
        if self.is_published and base:
            self.end_at = base + timedelta(days=self.duration_days)
        super().save(*args, **kwargs)

    @classmethod
    def live(cls):
        now = timezone.now()
        return cls.objects.filter(
            is_published=True, end_at__gte=now
        ).filter(Q(start_at__isnull=True) | Q(start_at__lte=now))
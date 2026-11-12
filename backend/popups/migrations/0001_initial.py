import uuid
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Popup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120, verbose_name="หัวข้อ")),
                ("message", models.TextField(blank=True, verbose_name="ข้อความ")),
                ("image", models.ImageField(blank=True, null=True, upload_to="popups/", verbose_name="รูป")),
                ("link_url", models.CharField(blank=True, max_length=500, verbose_name="ลิงก์เมื่อคลิกรูป")),
                ("duration_days", models.PositiveIntegerField(default=7, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(365)], verbose_name="แสดงกี่วัน")),
                ("start_at", models.DateTimeField(blank=True, help_text="เว้นว่าง = นับจากตอนกดเผยแพร่", null=True, verbose_name="เริ่มแสดง")),
                ("delay_seconds", models.PositiveIntegerField(default=3, help_text="รอหลังผู้ใช้เข้าหน้าเว็บกี่วินาที แล้วค่อยแสดง popup", validators=[django.core.validators.MaxValueValidator(60)], verbose_name="หน่วงก่อนแสดง (วินาที)")),
                ("auto_close_seconds", models.PositiveIntegerField(default=10, help_text="0 = ไม่จางหายเอง", validators=[django.core.validators.MaxValueValidator(120)], verbose_name="จางหายเองหลังกี่วินาที")),
                ("is_published", models.BooleanField(default=False, verbose_name="เผยแพร่")),
                ("published_at", models.DateTimeField(blank=True, editable=False, null=True)),
                ("end_at", models.DateTimeField(blank=True, editable=False, null=True)),
                ("preview_token", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
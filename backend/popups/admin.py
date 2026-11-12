from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin                   # จุดที่ 1: เพิ่มบรรทัดนี้

from .models import Popup


@admin.register(Popup)
class PopupAdmin(ModelAdmin):                         # จุดที่ 2: เปลี่ยนจาก admin.ModelAdmin
    list_display = ("title", "is_published", "duration_days", "published_at", "end_at")
    list_editable = ("is_published",)
    readonly_fields = ("preview_link", "published_at", "end_at")
    fields = ("title", "message", "image", "link_url", "duration_days", "start_at",
              "delay_seconds", "auto_close_seconds", "is_published",
              "published_at", "end_at", "preview_link")
    actions = ["stop_popups"]

    @admin.display(description="พรีวิว")
    def preview_link(self, obj):
        if not obj.pk:
            return "บันทึกก่อน แล้วลิงก์พรีวิวจะขึ้นที่นี่"
        base = getattr(settings, "FRONTEND_URL", "https://u-event.vercel.app")
        url = f"{base}/?popup_preview={obj.preview_token}"
        return format_html('<a href="{}" target="_blank">เปิดดูบนเว็บจริง</a>', url)

    @admin.action(description="หยุดแสดง popup ที่เลือก")
    def stop_popups(self, request, queryset):
        queryset.update(is_published=False)
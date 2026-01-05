# backend/users/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # ⭐ เพิ่ม faculty, gender, birthdate ใน list_display
    list_display = ['user', 'phone', 'faculty', 'gender', 'organizer_status', 'verification_link', 'created_at']
    list_filter = ['organizer_status', 'faculty', 'gender'] # เพิ่มตัวกรอง
    list_editable = ['organizer_status']
    search_fields = ['user__username', 'user__first_name', 'phone']

    def verification_link(self, obj):
        if obj.verification_doc:
            return format_html('<a href="{}" target="_blank" style="color:blue;">📄 ดูเอกสาร</a>', obj.verification_doc.url)
        return "-"
    verification_link.short_description = "เอกสารยืนยัน"
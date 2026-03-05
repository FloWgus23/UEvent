# backend/users/admin.py
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    # -------------------------------------------------------------
    # ⚙️ CONFIGURATION
    # -------------------------------------------------------------
    # เปิดให้แก้ไขสถานะได้ทันที (Dropdown ภาษาไทย)
    list_editable = ['organizer_status']
    
    # จัดเรียงคอลัมน์: รูป -> ข้อมูล user -> คณะ -> สถานะ -> เอกสาร -> วันที่สมัคร
    list_display = ['avatar_thumbnail', 'user_identity', 'faculty', 'organizer_status', 'verification_link', 'created_at']
    
    list_filter = ['organizer_status', 'faculty']
    search_fields = ['user__username', 'user__first_name', 'phone']

    # -------------------------------------------------------------
    # 🎨 VISUAL FUNCTIONS
    # -------------------------------------------------------------

    # 1. 🖼️ รูป Avatar (วงกลมมีขอบขาว)
    @display(description="Photo")
    def avatar_thumbnail(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
                obj.profile_image.url
            )
        # กรณีไม่มีรูป: สร้างวงกลมสีเทา + ตัวอักษรแรกของชื่อ
        return format_html(
            '<div style="width: 40px; height: 40px; border-radius: 50%; background-color: #f1f5f9; display: flex; align-items: center; justify-content: center; color: #64748b; font-weight: 600; border: 1px solid #e2e8f0;">{}</div>',
            obj.user.username[0].upper()
        )

    # 2. 🍎 User Identity (Apple Style: ชื่อเข้ม เบอร์เทา)
    @display(description="User Information")
    def user_identity(self, obj):
        phone = obj.phone if obj.phone else "-"
        return format_html(
            """
            <div class="flex flex-col justify-center h-full">
                <span class="font-semibold text-base text-slate-900 tracking-tight">{}</span>
                <span class="text-xs text-slate-500 font-medium flex items-center gap-1">
                    📱 {}
                </span>
            </div>
            """,
            obj.user.username,
            phone
        )

    # 3. 📎 Link ดูเอกสาร (Minimal Blue Link)
    def verification_link(self, obj):
        if obj.verification_doc:
            return format_html(
                """
                <a href="{}" target="_blank" 
                   class="inline-flex items-center gap-1 text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors duration-200 group">
                    <span class="group-hover:underline">เปิดดูเอกสาร</span>
                    <svg class="w-3 h-3" width="12" height="12" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="flex-shrink: 0;"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                </a>
                """, 
                obj.verification_doc.url
            )
        return format_html('<span class="text-slate-300 font-light">-</span>')
    verification_link.short_description = "Proof"
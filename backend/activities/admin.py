# backend/activities/admin.py
from django.contrib import admin
from .models import Activity, Registration, Tag, UserInterest, ActivityTag


# ========================================
# TAG SYSTEM ADMIN : แท็ก
# ========================================

#(จัดการแท็ก)
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('name', 'icon', 'color')
        }),
        ('รายละเอียด', {
            'fields': ('description', 'is_active')
        }),
    )


#(ดูความสนใจผู้ใช้)
@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['user', 'tag', 'explicit_score', 'implicit_score', 'total_score', 'last_updated']
    list_filter = ['tag', 'last_updated']
    search_fields = ['user__username', 'user__email', 'tag__name']
    ordering = ['-last_updated']
    readonly_fields = ['total_score', 'created_at', 'last_updated']
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('user', 'tag')
        }),
        ('คะแนน', {
            'fields': ('explicit_score', 'implicit_score', 'total_score')
        }),
        ('วันที่', {
            'fields': ('created_at', 'last_updated')
        }),
    )
    
    def total_score(self, obj):
        return f"{obj.total_score:.2f}"
    total_score.short_description = 'คะแนนรวม'


@admin.register(ActivityTag)
class ActivityTagAdmin(admin.ModelAdmin):
    list_display = ['activity', 'tag', 'created_at']
    list_filter = ['tag', 'created_at']
    search_fields = ['activity__name', 'tag__name']
    ordering = ['-created_at']


# ========================================
# ACTIVITY ADMIN : กิจกรรม 
# ========================================

class ActivityTagInline(admin.TabularInline):
    model = ActivityTag
    extra = 1
    verbose_name = 'แท็ก'
    verbose_name_plural = 'แท็ก'


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'registration_status', 'status', 'category', 'created_at']
    list_filter = ['status', 'category', 'date', 'created_at']
    search_fields = ['name', 'description', 'organizer', 'location']
    date_hierarchy = 'date'
    ordering = ['-created_at']
    
    inlines = [ActivityTagInline]
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('name', 'description', 'category')
        }),
        ('วันที่และเวลา', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        ('สถานที่และผู้จัด', {
            'fields': ('location', 'organizer')
        }),
        ('การลงทะเบียน', {
            'fields': ('capacity', 'registered_count', 'status')
        }),
        ('อื่นๆ', {
            'fields': ('tags', 'image'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['registered_count']


# ========================================
# REGISTRATION ADMIN : คนสมัคร
# ========================================

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'phone', 'status', 'registered_at']
    list_filter = ['status', 'registered_at', 'activity']
    search_fields = ['user__username', 'user__email', 'activity__name', 'phone']
    ordering = ['-registered_at']
    readonly_fields = ['registered_at']
    
    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('user', 'activity', 'status')
        }),
        ('ข้อมูลติดต่อ', {
            'fields': ('phone', 'note')
        }),
        ('วันที่', {
            'fields': ('registered_at',)
        }),
    )
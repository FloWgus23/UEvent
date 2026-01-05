# news/admin.py
from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'organization', 'created_at')
    search_fields = ('title', 'organization')
    list_filter = ('date',)

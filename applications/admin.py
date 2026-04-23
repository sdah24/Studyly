from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'university', 'program', 'status',
        'progress_percent', 'deadline', 'applied_date'
    ]
    list_filter  = ['status']
    search_fields = ['user__username', 'university__name']
    ordering = ['-applied_date']
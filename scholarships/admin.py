from django.contrib import admin
from .models import Scholarship


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'provider', 'funding_type', 'category',
        'deadline', 'recipients_per_year'
    ]
    list_filter = ['funding_type', 'category']
    search_fields = ['title', 'provider', 'description']
    ordering = ['deadline']
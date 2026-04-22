from django.contrib import admin
from .models import University, Program


class ProgramInline(admin.TabularInline):
    model = Program
    extra = 1


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    inlines = [ProgramInline]
    list_display = ['name', 'country', 'city', 'ranking', 'acceptance_rate', 'rating']
    list_filter = ['country']
    search_fields = ['name', 'city', 'country']
    ordering = ['ranking']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'level', 'duration', 'tuition_per_year']
    list_filter = ['level', 'university']
    search_fields = ['name', 'university__name']
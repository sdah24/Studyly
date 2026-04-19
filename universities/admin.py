from django.contrib import admin

from .models import University

# Register your models here.

admin.site.register(University)

class UniversityAdmin(admin.ModelAdmin):

    list_display = [

        "name",
        "country",
        "city",
        "ranking",

    ]

    search_fields = [

        "name",
        "country",

    ]

    list_filter = [

        "country",

    ]
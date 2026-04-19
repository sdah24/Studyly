from django.contrib import admin

from .models import Scholarship


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):

    list_display = [

        "title",
        "university",
        "amount",
        "deadline",

    ]

    search_fields = [

        "title",
        "university__name",

    ]

    list_filter = [

        "university",
        "deadline",

    ]
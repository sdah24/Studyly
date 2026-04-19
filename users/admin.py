from django.contrib import admin

# Register your models here.
# users/admin.py

from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        "user",
        "full_name",
        "phone_number",
        "created_at",
    ]
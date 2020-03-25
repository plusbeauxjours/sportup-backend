from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        ("None", {"fields": ("gender", "bio", "following",),},),
    )

    list_display = (
        "username",
        "uuid",
        "first_name",
        "last_name",
        "gender",
    )

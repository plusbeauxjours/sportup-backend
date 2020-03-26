from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        ("None", {"fields": ("gender", "bio", "following", "followers",),},),
    )

    list_display = (
        "username",
        "uuid",
        "first_name",
        "last_name",
        "gender",
    )


@admin.register(models.UserPlaysSport)
class UserPlaysSportAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "rating",
        "sport",
    )


@admin.register(models.UserRatesSport)
class UserRatesSportAdmin(admin.ModelAdmin):

    list_display = (
        "rater",
        "rated_user_sport",
        "rating",
    )
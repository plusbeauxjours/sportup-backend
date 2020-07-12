from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    fieldsets = UserAdmin.fieldsets + (
        (
            "None",
            {"fields": ("gender", "user_img", "bio", "following", "followers",),},
        ),
    )

    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "gender",
    )


@admin.register(models.UserPlaysSport)
class UserPlaysSportAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "rating",
        "sport",
    )


@admin.register(models.UserRatesSport)
class UserRatesSportAdmin(admin.ModelAdmin):

    list_display = ("id", "rater", "rated_user_sport", "rating", "rated_by")

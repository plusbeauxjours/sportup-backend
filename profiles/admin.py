from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from . import models


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()

        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


@admin.register(models.UserPlaysSport)
class UserPlaysSportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "sport",
        "rating",
    )


@admin.register(models.UserRatesUserSport)
class UserRatesUserSportAdmin(admin.ModelAdmin):
    list_display = ("id", "rater", "rated_user_sport", "rating")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

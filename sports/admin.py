from django.contrib import admin
from . import models


@admin.register(models.Sport)
class SportsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uuid",
        "name",
    )

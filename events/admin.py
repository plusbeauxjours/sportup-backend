from django.contrib import admin
from . import models


@admin.register(models.Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "sport",
        "name",
    )



@admin.register(models.Registration)
class EventsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "event",
        "registered_by",
        "approved",
    )



@admin.register(models.RegisteredPlayer)
class EventsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "registration",
    )


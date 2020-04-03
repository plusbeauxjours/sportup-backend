from django.contrib import admin
from . import models


@admin.register(models.Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "uuid",
        "owner",
        "sport",
        "name",
    )


@admin.register(models.Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "event",
        "registered_by",
        "approved",
    )


@admin.register(models.RegisteredPlayer)
class RegisteredPlayerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "registration",
    )

from django.contrib import admin
from .models import Event


class EventsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event, EventsAdmin)

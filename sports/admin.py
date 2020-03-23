from django.contrib import admin
from .models import Sport


class SportsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Sport, SportsAdmin)

from django.contrib import admin
from .models import Team


class TeamsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Team, TeamsAdmin)

from django.contrib import admin
from . import models


@admin.register(models.Team)
class TeamsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "team_name",
        "created_by",
        "rating",
    )


@admin.register(models.TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "team",
        "user",
        "is_admin",
    )


@admin.register(models.UserRatesTeam)
class UserRatesTeamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "team",
        "rating",
    )

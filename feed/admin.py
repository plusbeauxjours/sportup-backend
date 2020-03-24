from django.contrib import admin
from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "score",
        "text",
        "poster_by",
    )


@admin.register(models.UserPostInteraction)
class UserPostInteractionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post",
        "interaction",
    )

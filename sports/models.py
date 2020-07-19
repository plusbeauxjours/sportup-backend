from django.db import models
from core import models as core_models


class Sport(core_models.TimeStampedModel):
    name = models.CharField(max_length=20)
    sport_img_url = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return self.name

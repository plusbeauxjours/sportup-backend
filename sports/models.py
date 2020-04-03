import uuid
from django.db import models
from core import models as core_models


class Sport(core_models.TimeStampedModel):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, blank=True, null=True
    )
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

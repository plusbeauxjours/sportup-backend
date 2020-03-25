from django.db import models
from core import models as core_models


class Team(core_models.TimeStampedModel):
    name = models.CharField(max_length=50)
    rating = models.FloatField(blank=True, null=True)
    cover_img = models.ImageField(upload_to="team_cover_imgs/", blank=True, null=True)
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT)
    members = models.ManyToManyField("users.User", through="TeamMember")
    created_by = models.ForeignKey(
        "users.User", related_name="creator", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    rated_by = models.ManyToManyField(
        "users.User", related_name="rated", through="UserRatesTeam", blank=True
    )

    def __str__(self):
        return self.name


class TeamMember(core_models.TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class UserRatesTeam(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rating = models.IntegerField()

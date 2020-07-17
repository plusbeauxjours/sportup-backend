from django.db import models
from users import models as user_models
from sports import models as sport_models
from core import models as core_models
from django.db.models import Avg


class Team(core_models.TimeStampedModel):
    team_name = models.CharField(max_length=50)
    rating = models.FloatField(blank=True, null=True)
    cover_img = models.ImageField(upload_to="team_cover_imgs/", blank=True, null=True)
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT)
    members = models.ManyToManyField("users.User", through="TeamMember")
    created_by = models.ForeignKey(
        "users.User", related_name="creator", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.team_name

    def update_profile(self, team_name, sport_id):
        self.team_name = team_name
        if sport_id is not None:
            sport = sport_models.Sport.objects.get(id=sport_id)
            self.sport = sport

    def get_member_ids(self):
        tms = TeamMember.objects.filter(team=self)
        return [str(tm.user.id) for tm in tms]

    def add_members(self, member_ids):
        members = user_models.User.objects.filter(id__in=member_ids)
        for member in members:
            tm = TeamMember.objects.create(team=self, user=member)

    def remove_members(self, member_ids):
        members = user_models.User.objects.filter(id__in=member_ids)
        TeamMember.objects.filter(team=self, user__in=members).delete()

    def rating(self):
        avg = UserRatesTeam.objects.filter(team=self).aggregate(Avg("rating"))[
            "rating__avg"
        ]
        if avg:
            return round(avg, 1)


class TeamMember(core_models.TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class UserRatesTeam(core_models.TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rating = models.IntegerField()
    rated_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_rates_team_rated_by",
        blank=True,
    )

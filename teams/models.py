import uuid
from django.db import models
from users import models as user_models
from sports import models as sport_models
from core import models as core_models


class Team(core_models.TimeStampedModel):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, blank=True, null=True
    )
    team_name = models.CharField(max_length=50)
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
        return self.team_name

    def update_profile(self, team_name, sport_uuid):
        self.team_name = team_name
        if sport_uuid is not None:
            sport = sport_models.Sport.objects.get(uuid=sport_uuid)
            self.sport = sport

    def get_member_uuids(self):
        tms = TeamMember.objects.filter(team=self)
        return [str(tm.user.uuid) for tm in tms]

    def add_members(self, member_uuids):
        members = user_models.User.objects.filter(uuid__in=member_uuids)
        for member in members:
            tm = TeamMember.objects.create(team=self, user=member)

    def remove_members(self, member_uuids):
        members = user_models.User.objects.filter(uuid__in=member_uuids)
        TeamMember.objects.filter(team=self, user__in=members).delete()


class TeamMember(core_models.TimeStampedModel):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class UserRatesTeam(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    rating = models.IntegerField()

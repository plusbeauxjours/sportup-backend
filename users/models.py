from django.db import models
from django.contrib.auth.models import AbstractUser
from core import models as core_models
from sports import models as sport_models
from teams import models as team_models
from django.db.models import Avg


class User(AbstractUser):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )
    push_token = models.CharField(blank=True, null=True, max_length=200)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    user_img = models.ImageField(upload_to="user_imgs/", null=True, blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True
    )
    sports = models.ManyToManyField(
        "sports.Sport", through="UserPlaysSport", blank=True
    )

    def follow_user(self, user):
        self.following.add(user)

    def unfollow_user(self, user):
        self.following.remove(user)

    def get_sport_ids(self):
        ups = UserPlaysSport.objects.filter(user=self)
        return [obj.sport.id for obj in ups]

    def add_sports(self, sport_ids):
        sports = sport_models.Sport.objects.filter(pk__in=sport_ids)
        for sport in sports:
            ups = UserPlaysSport.objects.create(user=self, sport=sport)

    def remove_sports(self, sport_ids):
        sports = sport_models.Sport.objects.filter(pk__in=sport_ids)
        UserPlaysSport.objects.filter(user=self, sport__in=sports).delete()

    def has_sport(self, sport):
        try:
            ups = UserPlaysSport.objects.get(user=self, sport=sport)
            return True
        except UserPlaysSport.DoesNotExist:
            return False

    def rate_user_sport(self, user_id, sport_id, rating):
        sport = sport_models.Sport.objects.get(id=sport_id)
        user = User.objects.get(id=user_id)
        ups = UserPlaysSport.objects.get(user=user, sport=sport)
        try:
            urus = UserRatesSport.objects.get(
                rater=user, rated_user_sport=ups, rated_by=self
            )
            urus.rating = rating
            urus.save()
        except UserRatesSport.DoesNotExist:
            urus = UserRatesSport.objects.create(
                rater=user, rated_user_sport=ups, rating=rating, rated_by=self
            )

    def rate_team(self, team_id, rating):
        team = team_models.Team.objects.get(id=team_id)
        try:
            urut = team_models.UserRatesTeam.objects.get(team=team, rated_by=self)
            urut.rating = rating
            urut.save()
        except team_models.UserRatesTeam.DoesNotExist:
            urut = team_models.UserRatesTeam.objects.create(
                team=team, rated_by=self, rating=rating
            )

    def is_team_admin(self, team):
        try:
            tm = team_models.TeamMember.objects.get(user=self, team=team)
            return tm.is_admin
        except team_models.TeamMember.DoesNotExist:
            return False


class UserPlaysSport(core_models.TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="UserPlaysSport_user",
    )
    sport = models.ForeignKey("sports.Sport", on_delete=models.CASCADE)

    def rating(self):
        avg = UserRatesSport.objects.filter(rater=self.user).aggregate(Avg("rating"))[
            "rating__avg"
        ]
        if avg:
            return round(avg, 1)

    def __str__(self):
        return self.sport.name


class UserRatesSport(core_models.TimeStampedModel):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rater")
    rated_user_sport = models.ForeignKey(
        UserPlaysSport, related_name="rated_user_sport_user", on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    rated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_rates_sport_rated_by",
        blank=True,
    )

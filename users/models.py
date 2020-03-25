from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from core import models as core_models
from sports import models as sport_models


class User(AbstractUser):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, blank=True, null=True
    )
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    user_img = models.ImageField(upload_to="user_imgs/", null=True, blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField("self", related_name="followers", blank=True)
    sports = models.ManyToManyField(
        "sports.Sport", through="UserPlaysSport", blank=True
    )

    def follow_user(self, user):
        self.following.add(user)

    def unfollow_user(self, user):
        self.following.remove(user)

    def add_sports(self, sports_ids):
        sports = sport_models.Sport.objects.filter(pk__in=sports_ids)
        for sport in sports:
            ups = UserPlaysSport.objects.create(user=self, sport=sport)

    def remove_sports(self, sport_ids):
        sports = sport_models.Sport.objects.filter(pk__in=sport_ids)
        UserPlaysSport.objects.filter(user=self, sport__in=sports).delete()


class UserPlaysSport(core_models.TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="UserPlaysSport_user",
    )
    rating = models.FloatField(blank=True, null=True)
    sport = models.ForeignKey("sports.Sport", on_delete=models.CASCADE)
    rated_by = models.ManyToManyField(
        User,
        through="UserRatesSport",
        blank=True,
        related_name="UserPlaysSport_rated_by",
    )


class UserRatesSport(core_models.TimeStampedModel):
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_user_sport = models.ForeignKey(UserPlaysSport, on_delete=models.CASCADE)
    rating = models.IntegerField()

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
    followers = models.ManyToManyField("self", related_name="following", blank=True)
    sports = models.ManyToManyField(
        "sports.Sport", through="UserPlaysSport", blank=True
    )

    def followers_count(self):
        return self.followers.all().count()

    def following_count(self):
        return self.following.all().count()

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
        except models.ObjectDoesNotExist:
            return False

    def rate_user_sport(self, uuid, sport_id, rating):
        sport = sport_models.Sport.objects.get(pk=sport_id)
        user = User.objects.get(uuid=uuid)
        ups = UserPlaysSport.objects.get(user=user, sport=sport)

        try:
            urus = UserRatesSport.objects.get(rater=user, rated_user_sport=ups)
            urus.rating = rating
            urus.save()
        except UserRatesSport.DoesNotExist:
            urus = UserRatesSport.objects.create(
                rater=user, rated_user_sport=ups, rating=rating
            )


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

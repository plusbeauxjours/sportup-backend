from django.db import models
from sports import models as sport_models
from core import models as core_models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="profile_imgs/", null=True, blank=True)
    bio = models.TextField(blank=True)
    following = models.ManyToManyField(User, related_name="follwers", blank=True)
    sports = models.ManyToManyField(
        sport_models.Sport, through="UserPlaysSport", blank=True
    )


class userPlaysSport(core_models.TimeStampedModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sport = models.ForeignKey(sport_models.Sport, on_delete=models.CASCADE)
    rating = models.FloatField(blank=True, null=True)

    rated_by = models.ManyToManyField(User, through="UserRatesUserSport", blank=True)


class UserRatesUserSport(core_models.TimeStampedModel):
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_user_sport = models.ForeignKey(userPlaysSport, on_delete=models.CASCADE)
    rating = models.IntegerField()

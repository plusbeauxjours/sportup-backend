from django.db import models
from core import models as core_models


class Event(core_models.TimeStampedModel):
    name = models.TextField()

    description = models.TextField(blank=True, null=True)
    cover_img = models.ImageField(upload_to="event_cover_imgs/", blank=True, null=True)
    document = models.FileField(upload_to="event_docs/", blank=True, null=True)
    sport = models.ForeignKey("sports.Sport", on_delete=models.PROTECT)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    minimum_members = models.IntegerField()
    maximum_members = models.IntegerField()
    expected_teams = models.IntegerField()
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Registration(models.Model):
    name = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_by = models.ForeignKey("users.User", on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    captain_name = models.CharField(max_length=20)
    captain_cnic = models.CharField(max_length=15)
    captain_contact_num = models.CharField(max_length=12)


class RegisteredPlayer(models.Model):
    name = models.CharField(max_length=20)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

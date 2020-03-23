from django.db import models
from django.contrib.auth.models import User
from core import models as core_models


class Post(core_models.TimeStampedModel):
    poster_by = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    post_img = models.ImageField(upload_to="post_imgs/", blank=True, null=True)
    score = models.IntegerField(default=0)
    interactions = models.ManyToManyField(
        User, related_name="interacts", through="UserPostInteraction", blank=True
    )

    class Meta:
        ordering = ["created_at"]


class UserPostInteraction(core_models.TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    INTERACTION_CHOICES = (("UV", "Upvote"), ("DV", "Downvote"))
    interaction = models.CharField(
        max_length=2, choices=INTERACTION_CHOICES, blank=True, null=True
    )

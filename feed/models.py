from django.db import models
from core import models as core_models


class Post(core_models.TimeStampedModel):
    posted_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="post"
    )
    text = models.TextField(blank=True, null=True)
    post_img = models.ImageField(upload_to="post_imgs/", blank=True, null=True)
    score = models.IntegerField(default=0)
    interactions = models.ManyToManyField(
        "users.User",
        related_name="interacts",
        through="UserPostInteraction",
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text


class UserPostInteraction(core_models.TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    INTERACTION_CHOICES = (("UV", "Upvote"), ("DV", "Downvote"))
    interaction = models.CharField(
        max_length=2, choices=INTERACTION_CHOICES, blank=True, null=True
    )

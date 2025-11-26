from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_subscribed = models.BooleanField(
        default=False, help_text="Tracks if the auth user wants email updates."
    )
    bio = models.TextField(
        null=True, blank=True, help_text="Optional profile bio for the Author or Users."
    )

    def __str__(self):
        return self.username

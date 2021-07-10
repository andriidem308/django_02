"""Account Models."""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """User Class."""

    email = models.EmailField('email address', blank=False, null=False, unique=True)
    confirmation_token = models.UUIDField(default=uuid.uuid4)


def user_avatar_upload(instance, filename):
    """Upload user avatar."""
    return f'{instance.user_id}/{filename}'


class Avatar(models.Model):
    """Avatar class."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.ImageField(upload_to=user_avatar_upload)


class Profile(models.Model):
    """Profile class."""

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_picture = models.ImageField(null=True, blank=True, upload_to=user_avatar_upload)
    website_url = models.URLField(max_length=255, null=True, blank=True)
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    instagram_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        """Print Profile."""
        return str(self.user)

    @staticmethod
    def get_absolute_url():
        """Set absolute link."""
        return reverse('homepage')

    def delete(self, **kwargs):
        """Delete in custom method for cache_page."""
        super().delete()

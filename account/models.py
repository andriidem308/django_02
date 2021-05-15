"""Account Models."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User Class."""

    email = models.EmailField('email address', blank=False, null=False, unique=True)

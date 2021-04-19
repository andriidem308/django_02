"""Signals module."""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Author


@receiver(pre_save, sender=Author)
def author_pre_save(sender, instance, **kwargs):
    """Signal Author Pre Save."""
    print('*** Pre Save ***')
    instance.name = instance.name.lower()
    instance.email = instance.email


@receiver(post_save, sender=Author)
def author_post_save(sender, instance, created, **kwargs):
    """Signal Post Save."""
    print('*** Post Save ***')
    if created:
        print("Created")
    else:
        print('Exist')

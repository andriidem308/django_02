"""Celery Tasks."""
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now
from main.models import Logger, Subscriber
from main.services.notify_service import email_send


@shared_task
def delete_logs_sync():
    """Delete 3-days-logs."""
    Logger.objects.filter(created=now() - timedelta(days=3)).delete()


@shared_task
def notify_subscriber_sync(email):
    """Notify Subscriber."""
    email_send(email)


@shared_task
def notify_subscribers():
    """Notify All Subscribers."""
    subscribers = Subscriber.objects.values_list('email_to', flat=True)

    for sub in subscribers:
        email_send(sub)

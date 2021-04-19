"""Celery Class."""
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_02.settings')

app = Celery('django_02')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

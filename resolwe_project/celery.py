"""Celery configuration."""
import os

try:
    from celery import Celery
except ImportError:
    Celery = None

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resolwe_project.settings")

app = None
if Celery:
    app = Celery('resolwe_project')

    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


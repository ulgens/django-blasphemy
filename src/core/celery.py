import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("blasphemy")

# Configure Celery using settings from Django settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load tasks
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(("core",))

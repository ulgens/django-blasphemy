# Celery app needs to be imported for its initialization
from .celery import app as celery_app

__all__ = ("celery_app",)

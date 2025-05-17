"""
Test tasks
"""

from celery import shared_task


@shared_task
def test_task(arg1, arg2):
    return arg1 + arg2


@shared_task
def beat_task():
    print("Hello Celery!")  # noqa: T201

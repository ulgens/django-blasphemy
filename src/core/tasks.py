"""
Test tasks
"""

from celery import shared_task


@shared_task
def test_task(arg1, arg2):  # noqa: FURB118
    return arg1 + arg2

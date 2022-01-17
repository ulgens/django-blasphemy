from django.urls import path

import logging

logger = logging.getLogger(__name__)


def error(request):
    1 / 0


def manual_log(request):
    try:
        1 / 0
    except Exception as error:
        logger.exception(error)
        raise error


def manual_flat_log(request):
    try:
        1 / 0
    except Exception as error:
        logger.exception(str(error))
        raise error

"""
Test views
"""

import logging

logger = logging.getLogger(__name__)


def error(request):
    return 1 / 0


def manual_log(request):
    try:
        return 1 / 0
    except ZeroDivisionError:
        logger.exception("Manually logged exception")
        raise


def manual_flat_log(request):
    try:
        return 1 / 0
    except ZeroDivisionError as e:
        flat_log = str(e)
        logger.exception(flat_log)
        raise

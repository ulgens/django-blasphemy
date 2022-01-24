import logging

logger = logging.getLogger(__name__)


def error(request):
    1 / 0


def manual_log(request):
    try:
        1 / 0
    except Exception as e:
        logger.exception(e)
        raise error


def manual_flat_log(request):
    try:
        1 / 0
    except Exception as e:
        logger.exception(str(e))
        raise error

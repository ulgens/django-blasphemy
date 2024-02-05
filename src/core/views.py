import logging

logger = logging.getLogger(__name__)


def error(request):
    return 1 / 0


def manual_log(request):
    try:
        return 1 / 0
    except Exception as e:
        logger.exception(e)
        raise e


def manual_flat_log(request):
    try:
        return 1 / 0
    except Exception as e:
        logger.exception(str(e))
        raise e

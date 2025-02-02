from collections.abc import Mapping

from django.core import exceptions as django_exceptions
from rest_framework import exceptions as drf_exceptions
from rest_framework.fields import get_error_detail
from rest_framework.settings import api_settings as drf_settings
from rest_framework.views import exception_handler as orig_exception_handler

__all__ = ("exception_handler",)


def convert_django_permission_denied(exc):
    """
    Converts Django's PermissionDenied exception to DRF's PermissionDenied exception.
    """

    # str(exc) doesn't seem to be the best solution, but we don't have exc.message here.
    return drf_exceptions.PermissionDenied(detail=str(exc))


def convert_django_validation_error(exc):
    """
    Converts Django's ValidationError exception to DRF's ValidationError exception.

    This is a modified version of DRF's `serializers.as_serializer_error()` function.
    DRF's version doesn't convert from {"__all__": error/s} to {"non_field_errors": error/s]},
    which is a common case with Django's model layer validation errors.
    """

    detail = get_error_detail(exc)

    if isinstance(detail, Mapping):
        if "__all__" in detail:
            detail[drf_settings.NON_FIELD_ERRORS_KEY] = detail["__all__"]
            del detail["__all__"]

        # If errors may be a dict we use the standard {key: list of values}.
        # Here we ensure that all the values are *lists* of errors.
        details = {}

        for key, value in detail.items():
            details[key] = value if isinstance(value, list) else [value]

    elif isinstance(detail, list):
        # Errors raised as a list are non-field errors.
        details = {drf_settings.NON_FIELD_ERRORS_KEY: detail}

    else:
        # Errors raised as a string are non-field errors.
        details = {drf_settings.NON_FIELD_ERRORS_KEY: [detail]}

    return drf_exceptions.ValidationError(detail=details)


def exception_handler(exc, context):
    """
    Automatically converts Django's model layer PermissionDenied
    and ValidationError exceptions to their DRF counterparts.
    """

    # Carry over PermissionDenied reason message from model layer to DRF
    if isinstance(exc, django_exceptions.PermissionDenied):
        exc = convert_django_permission_denied(exc)

    # Carry over ValidationError from model layer to DRF
    elif isinstance(exc, django_exceptions.ValidationError):
        exc = convert_django_validation_error(exc)

    response = orig_exception_handler(exc, context)

    return response

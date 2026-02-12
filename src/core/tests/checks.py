# TODO:
#   How to test system checks?
#   https://docs.djangoproject.com/en/stable/topics/checks/#writing-tests

import importlib
import inspect
from pathlib import Path
from unittest import TestCase as AbsoluteBaseTestCase

from django.apps import apps
from django.conf import settings
from django.core.checks import Warning, register  # noqa: A004
from django.test import SimpleTestCase as BaseDjangoTestCase
from rest_framework.test import APITestCase as BaseAPITestCase

from core.testcases import APITestCase, TestCase


def is_test_case(obj):
    return inspect.isclass(obj) and issubclass(obj, AbsoluteBaseTestCase)


def get_test_cases(app_config):
    # TODO: Can we use the test runner instead?
    test_file_paths = Path(app_config.path).rglob("*test*.py")
    test_cases = []

    for abs_path in test_file_paths:
        rel_path = abs_path.relative_to(settings.BASE_DIR)
        module_parts = rel_path.with_suffix("").parts
        module_name = ".".join(module_parts)

        # TODO: Try to import module directly from the path
        module = importlib.import_module(module_name)

        for _, obj in inspect.getmembers(module, is_test_case):
            # Ignore imported objects
            if obj.__module__ != module.__name__:
                continue

            test_cases.append(obj)

    return test_cases


def check_W001_test_base(test_case):  # noqa: N802
    """
    All test cases should inherit from core.testcases.TestCase,
    except for API test cases.
    """
    # No need to check base test cases
    if test_case.__module__ == "core.testcases":
        return None

    # Expected & valid case
    if issubclass(test_case, TestCase):
        return None

    msg = f"{test_case.__module__}.{test_case.__name__} does not inherit from core.testcases.TestCase"
    warning = Warning(
        msg,
        obj=test_case,
        id="tests.W001",
    )

    return warning


def check_W002_api_test_base(test_case):  # noqa: N802
    """
    All API test cases should inherit from core.testcases.APITestCase
    """
    # No need to check base test cases
    if test_case.__module__ == "core.testcases":
        return None

    # Expected & valid case
    if issubclass(test_case, APITestCase):
        return None

    msg = f"{test_case.__module__}.{test_case.__name__} does not inherit from core.testcases.APITestCase"
    warning = Warning(
        msg,
        obj=test_case,
        id="tests.W002",
    )

    return warning


@register()
def check_base_test_case(app_configs, **kwargs):
    """
    Ensure all test case classes inherit from custom base test cases.
    """
    warnings = []

    if not app_configs:
        app_configs = (apps.get_app_config(app_label) for app_label in settings.INTERNAL_APPS)

    for app_config in app_configs:
        test_cases = get_test_cases(app_config)

        for test_case in test_cases:
            warning = None

            # Most specific/narrower checks should be placed higher
            if issubclass(test_case, BaseAPITestCase):
                warning = check_W002_api_test_base(test_case)

            elif issubclass(test_case, BaseDjangoTestCase):
                warning = check_W001_test_base(test_case)

            if warning:
                warnings.append(warning)

    # TODO: Should we order warnings by test by ID?
    return warnings

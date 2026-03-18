from typing import Literal
from unittest import SkipTest

from django.db import connection
from django.test import Client
from django.test import TestCase as BaseTestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase as BaseAPITestCase
from unittest_parametrize import ParametrizedTestCase

from users.factories import UserFactory

__all__ = (
    "APITestCase",
    "AdminTestCase",
    "TestCase",
)


class TestCase(ParametrizedTestCase, BaseTestCase):
    pass


class AdminTestCase(TestCase):
    app_name = None
    model_name = None

    @classmethod
    def setUpClass(cls):
        if cls.__name__.endswith("AdminTestCase"):
            skip_msg = f"{cls.__name__} is an abstract base class"
            raise SkipTest(skip_msg)
        else:
            super().setUpClass()

    def setUp(self) -> None:
        self.user = UserFactory(is_staff=True, is_superuser=True)

        self.client = Client()
        self.client.force_login(user=self.user)

        add_viewname = f"admin:{self.app_name}_{self.model_name}_add"
        self.add_url = reverse(add_viewname)

        changelist_viewname = f"admin:{self.app_name}_{self.model_name}_changelist"
        self.changelist_url = reverse(changelist_viewname)

    def test_add_url(self):
        self.assertEqual(
            self.add_url,
            f"/admin/{self.app_name}/{self.model_name}/add/",
        )

    def test_add(self):
        response = self.client.get(self.add_url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_changelist_url(self):
        self.assertEqual(
            self.changelist_url,
            f"/admin/{self.app_name}/{self.model_name}/",
        )

    def test_changelist(self):
        response = self.client.get(self.changelist_url)

        self.assertEqual(
            response.status_code,
            200,
        )


checked_methods_type = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


class APITestCase(ParametrizedTestCase, BaseAPITestCase):
    @classmethod
    def setUpClass(cls):
        if cls.__name__ == "APITestCase":
            skip_msg = "APITestCase is an abstract base class"
            raise SkipTest(skip_msg)

        super().setUpClass()

        cls.detail_url: str = ""
        cls.detail_not_allowed_methods: list[checked_methods_type] = []
        cls.list_url: str = ""
        cls.list_not_allowed_methods: list[checked_methods_type] = []

    def _assert_not_allowed_methods(
        self,
        url: str,
        methods: list[checked_methods_type],
    ) -> None:
        for method in methods:
            with CaptureQueriesContext(connection) as db_ctx:
                # Run the request
                resp = self.client.generic(method, url)

            # Check the response
            self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

            # Check the db queries
            self.assertEqual(len(db_ctx), 0)

    # TODO: Can this be parameterized?
    # TODO: What happens when not allowed method list is empty? Still showing on the test report?
    def test_detail_not_allowed_methods(self):
        self._assert_not_allowed_methods(
            url=self.detail_url,
            methods=self.detail_not_allowed_methods,
        )

    # TODO: Can this be parameterized?
    # TODO: What happens when not allowed method list is empty? Still showing on the test report?
    def test_list_not_allowed_methods(self):
        self._assert_not_allowed_methods(
            url=self.list_url,
            methods=self.list_not_allowed_methods,
        )

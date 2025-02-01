from unittest import SkipTest

from django.test import Client, TestCase
from django.urls import reverse

from users.factories import UserFactory


class AdminTestCase(TestCase):
    app_name = None
    model_name = None

    @classmethod
    def setUpClass(cls):
        if cls.__name__.endswith("AdminTestCase"):
            skip_msg = f"{cls.__name__} is an abstract base class"
            raise SkipTest(skip_msg)
        else:
            super(__class__, cls).setUpClass()

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

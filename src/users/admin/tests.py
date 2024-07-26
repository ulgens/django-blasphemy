from django.test import Client, TestCase, tag
from django.urls import reverse

from users.factories import UserFactory


@tag("admin", "snippet")
class UserAdminTest(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory(is_staff=True, is_superuser=True)

        self.client = Client()
        self.client.force_login(user=self.user)

        self.viewname = "admin:users_user_changelist"
        self.url = reverse(self.viewname)

    def test_url(self):
        expected_url = "/admin/users/user/"

        self.assertEqual(self.url, expected_url)

    def test_changelist(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from faker import Faker
from parameterized import parameterized

from core.tests.utils import CASE_FUNCTIONS

from ..factories import UserFactory  # noqa: TID252
from .utils import denormalize_email

fake = Faker()
User = get_user_model()


class UserEmailTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = fake.email()
        cls.user = UserFactory(
            email=cls.email,
        )

    @parameterized.expand(CASE_FUNCTIONS.values())
    def test_normalize(self, case_method):
        """
        User.email should be normalized.
        """
        email = denormalize_email(self.email, case_method)

        with self.assertRaisesMessage(
            IntegrityError,
            'duplicate key value violates unique constraint "users_user_email_key"',
        ):
            UserFactory(email=email)

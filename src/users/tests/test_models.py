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

        django.contrib.auth.base_user.BaseUserManager.normalize_email:
            Normalize the email address by lowercasing the domain part of it.
        """
        email = denormalize_email(
            fake.free_email(),
            case_method,
        )
        user = UserFactory(email=email)

        domain = user.email.split("@")[1]
        self.assertEqual(domain, domain.lower())

    @parameterized.expand(CASE_FUNCTIONS.values())
    def test_ci_lookup(self, case_method):
        """
        User.email lookup should be case-insensitive.
        """
        cased_email = case_method(self.email)

        self.assertEqual(
            User.objects.filter(email=cased_email).count(),
            1,
        )
        self.assertEqual(User.objects.get(email=cased_email), self.user)

    @parameterized.expand(CASE_FUNCTIONS.values())
    def test_ci_unique(self, case_method):
        """
        User.email uniqueness should be case-insensitive.
        """
        cased_email = case_method(self.email)

        with self.assertRaisesMessage(
            expected_exception=IntegrityError,
            expected_message='duplicate key value violates unique constraint "users_user_email_key"',
        ):
            UserFactory(email=cased_email)

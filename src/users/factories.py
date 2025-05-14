import factory
from django.contrib.auth import get_user_model
from faker import Faker

from core.faker_providers import E164Provider

__all__ = ("UserFactory",)

fake = Faker()
fake.add_provider(E164Provider)

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    phone_number = factory.LazyAttribute(lambda _: fake.e164())
    password = factory.django.Password(fake.password(length=16))

    @factory.lazy_attribute
    def email(self):
        """
        Adds a random number suffix to the local part of the email to ensure uniqueness.
        Using 'free_email' alone can cause duplicate data.

        factory.Transformer is not used here because we don't want to transform the value if it's explicitly set.
        """

        email = fake.free_email()

        email_parts = email.split("@")
        number_suffix = fake.random_number(digits=3)

        unique_email = f"{email_parts[0]}{number_suffix}@{email_parts[1]}"

        return unique_email

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    class Meta:
        model = User

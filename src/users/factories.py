import factory
from faker import Faker

from .models import User

__all__ = ("UserFactory",)

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    # Using 'free_email' alone can cause duplicate data.
    email = factory.LazyFunction(lambda: f"{fake.random_number(digits=3)}{fake.free_email()}")
    username = factory.LazyFunction(lambda: f"{fake.user_name()}{fake.random_number(digits=3)}")
    password = factory.django.Password(fake.password(length=16))

    class Meta:
        model = User

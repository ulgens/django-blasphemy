import factory
from faker import Faker

from .models import User

__all__ = ("UserFactory",)

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    # Using 'free_email' alone can cause duplicate data.
    email = factory.LazyFunction(lambda: f"{fake.random_number(digits=3)}{fake.free_email()}")
    password = factory.django.Password(fake.password(length=16))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)

    class Meta:
        model = User

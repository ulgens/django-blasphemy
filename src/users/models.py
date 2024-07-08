from django.contrib.auth.models import AbstractUser

from core.models import BaseModel


class User(BaseModel, AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

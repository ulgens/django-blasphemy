from django.contrib.auth.models import AbstractUser

from core.db.models import BaseModel


class User(BaseModel, AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

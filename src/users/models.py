from core.models import BaseModel
from django.contrib.auth.models import AbstractUser


class User(BaseModel, AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

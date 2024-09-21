from gettext import gettext as _

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.db.models import BaseModel

from .managers import UserManager


class User(BaseModel, AbstractUser):
    """
    Improved user model with
    - no username & login with email
    - full_name and short_name instead of first_name and last_name

    The implementation is inspired by:
    - django-improved-user
        - Homepage: https://github.com/jambonsw/django-improved-user
        - Not maintained anymore
    - django-authtools
        - Homepage: https://github.com/fusionbox/django-authtools
        - Not properly maintained. A potential security issue is open since 2013:
            https://github.com/fusionbox/django-authtools/issues/2
    """

    # Disable unused fields from AbstractUser
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(
        _("email address"),
        unique=True,
        db_collation="case_insensitive",
    )
    full_name = models.CharField(
        _("full name"),
        max_length=200,
        blank=True,
    )
    short_name = models.CharField(
        _("short name"),
        max_length=50,
        blank=True,
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    # misnomer; fields Django prompts for when user calls createsuperuser
    # https://docs.djangoproject.com/en/stable/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = ("full_name", "short_name")

    def clean(self):
        """
        Override default clean method to normalize email.
        """
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    class Meta(AbstractBaseUser.Meta):
        swappable = "AUTH_USER_MODEL"

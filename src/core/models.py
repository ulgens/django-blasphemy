import uuid_extensions
from django.db import models

__all__ = ("BaseModel",)


# TODO:
#    * Make use of db_default: https://docs.djangoproject.com/en/5.0/ref/models/fields/#db-default
#    * Check RandomUUID for Postgres: https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/functions/#randomuuid
class UUIDModel(models.Model):
    id = models.UUIDField(
        default=uuid_extensions.uuid7,
        editable=False,
        primary_key=True,
        verbose_name="ID",
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    # TODO: Make use of db_default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UUIDModel):
    class Meta:
        abstract = True

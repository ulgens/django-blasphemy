import uuid

from django.db import models

__all__ = ("BaseModel",)


class UUIDModel(models.Model):
    # TODO: Make use of db_default
    id = models.UUIDField(
        default=uuid.uuid4,
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

import uuid_extensions
from dirtyfields import DirtyFieldsMixin
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


class BaseModel(DirtyFieldsMixin, TimeStampedModel, UUIDModel):
    class Meta:
        abstract = True

    def save_dirty_fields(self):
        """
        Save only the dirty fields.

        Fields with auto_now=True never gets dirty.
        We need to add them to the update_fields list manually if anything else is dirty.

        https://github.com/romgar/django-dirtyfields/issues/195
        """

        if self._state.adding:
            self.save()
            return

        dirty_fields = self.get_dirty_fields(check_relationship=True)
        update_fields = list(dirty_fields.keys())

        if not update_fields:
            return

        # auto_now fields never get dirty, they need to be added manually
        auto_now_fields = [f.name for f in self._meta.fields if getattr(f, "auto_now", False)]
        update_fields.extend(auto_now_fields)

        self.save(update_fields=update_fields)

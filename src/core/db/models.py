import struct
from datetime import datetime
from uuid import uuid7

from dirtyfields import DirtyFieldsMixin
from django.db import models
from django.utils.timezone import get_current_timezone

__all__ = ("BaseModel",)

NANOSECONDS_PER_SECOND = 1_000_000_000


# TODO:
#    * Make use of db_default: https://docs.djangoproject.com/en/dev/ref/models/fields/#db-default
#    * Check RandomUUID for Postgres: https://docs.djangoproject.com/en/dev/ref/contrib/postgres/functions/#randomuuid
class UUIDModel(models.Model):
    id = models.UUIDField(
        default=uuid7,
        editable=False,
        primary_key=True,
        verbose_name="ID",
        help_text="The unique identifier of the record, in UUIDv7 format.",
    )

    class Meta:
        abstract = True

    # TODO: Try to make use of `models.GeneratedField`
    # TODO: Consider using this method to replace `created_at` field
    def get_created_at_from_id(self):
        # > UUIDv7 features a time-ordered value field derived from the widely implemented and well-known
        # > Unix Epoch timestamp source, the number of milliseconds since midnight 1 Jan 1970 UTC, leap seconds excluded.
        # https://www.rfc-editor.org/rfc/rfc9562.html#name-uuid-version-7
        epoch_ms = self.id.time

        # Unix time (timestamp) is defined in seconds
        # https://developer.mozilla.org/en-US/docs/Glossary/Unix_time
        timestamp = epoch_ms / 1000

        created_at = datetime.fromtimestamp(
            timestamp,
            tz=get_current_timezone(),
        )

        # uuid7 (uuid_extensions) package was using an outdated implementation for UUIDv7
        # There is no clear way to detect which UUID values are generated via the package.
        # During the manual discovery, 2025-09-18 was converted as 2198-03-14 so roughly speaking,
        # any result beyond year 2195 can be accepted as wrong.
        # This block can be removed when all stored buggy UUID values are replaced or deleted.
        # https://github.com/stevesimmons/uuid7/issues/1
        if created_at.year > 2195:
            # Adapted from uuid_extensions buggy version
            # https://github.com/stevesimmons/uuid7/blob/7cd40cd9be0affa1cd09e7476e29af555c678220/uuid_extensions/uuid7.py#L262
            bits = struct.unpack(">IHHHHI", self.id.bytes)
            whole_secs = (bits[0] << 4) + (bits[1] >> 12)
            frac_binary = ((bits[1] & 0x0FFF) << 26) + ((bits[2] & 0x0FFF) << 14) + (bits[3] & 0x3FFF)
            frac_ns, _ = divmod(frac_binary * NANOSECONDS_PER_SECOND, 1 << 38)
            epoch_ns = whole_secs * NANOSECONDS_PER_SECOND + frac_ns

            timestamp = epoch_ns / NANOSECONDS_PER_SECOND

            created_at = datetime.fromtimestamp(timestamp, tz=get_current_timezone())

        return created_at


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

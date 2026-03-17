import uuid

import dirtyfields.dirtyfields
import django.utils.timezone
import phonenumber_field.modelfields
from django.contrib.postgres.operations import CreateCollation
from django.db import migrations, models

import users.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = (("auth", "0012_alter_user_first_name_max_length"),)

    operations = (
        # Creates a collation for case-insensitive text in PostgreSQL,
        # to replace Django's CI* fields.
        # https://adamj.eu/tech/2023/02/23/migrate-django-postgresql-ci-fields-case-insensitive-collation
        CreateCollation(
            "case_insensitive",
            provider="icu",
            locale="und-u-ks-level2",
            deterministic=False,
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid7,
                        editable=False,
                        help_text="The unique identifier of the record, in UUIDv7 format.",
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "email",
                    models.EmailField(
                        db_collation="case_insensitive", max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=16, region=None),
                ),
                ("full_name", models.CharField(blank=True, max_length=200, verbose_name="full name")),
                ("short_name", models.CharField(blank=True, max_length=50, verbose_name="short name")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
                "swappable": "AUTH_USER_MODEL",
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
            managers=[
                ("objects", users.managers.UserManager()),
            ],
        ),
    )

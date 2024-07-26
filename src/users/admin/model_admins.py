from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = list(BaseUserAdmin.list_display)  # noqa: RUF012
    list_display.remove("username")

    search_fields = list(BaseUserAdmin.search_fields)  # noqa: RUF012
    search_fields.remove("username")

    add_form = UserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "short_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    fieldsets = (
        (
            None,
            {"fields": ("email", "password")},
        ),
        (
            _("Personal info"),
            {"fields": ("full_name", "short_name")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined")},
        ),
        (
            _("System timestamps"),
            {"fields": ("created_at", "updated_at")},
        ),
    )
    readonly_fields = (
        "last_login",
        "date_joined",
        "created_at",
        "updated_at",
    )
    ordering = ("email",)

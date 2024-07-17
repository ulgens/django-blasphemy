from gettext import gettext as _

from django.contrib import admin

from snippets.models import Snippet

__all__ = ("SnippetAdmin",)


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "language",
        "style",
    )
    search_fields = (
        "id",
        "title",
        "code",
    )
    list_filter = (
        "language",
        "style",
    )

    fieldsets = (
        (
            None,
            {
                "fields": ("id", "title", "language", "style", "code"),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

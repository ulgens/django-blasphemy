from django.contrib import admin

from .models import Snippet


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
    fields = (
        "id",
        "created_at",
        "updated_at",
        "title",
        "language",
        "style",
        "code",
    )
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

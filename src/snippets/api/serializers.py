from rest_framework import serializers

from ..models import Snippet

__all__ = ("SnippetSerializer",)


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = (
            "id",
            "title",
            "code",
            "language",
            "style",
        )

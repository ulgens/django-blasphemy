from rest_framework import serializers

from ..models import Snippet  # noqa: TID252


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

from rest_framework import serializers

__all__ = (
    "GitRefSerializer",
    "IsAliveSerializer",
)


class GitRefSerializer(serializers.Serializer):
    branch = serializers.CharField(allow_null=True)
    commit_sha = serializers.CharField()


class IsAliveSerializer(serializers.Serializer):
    is_alive = serializers.BooleanField()

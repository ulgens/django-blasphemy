from rest_framework import serializers

__all__ = ("IsAliveSerializer",)


class IsAliveSerializer(serializers.Serializer):
    is_alive = serializers.BooleanField()

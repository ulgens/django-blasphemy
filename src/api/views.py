from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import IsAliveSerializer

__all__ = ("IsAliveView",)


@extend_schema(tags=["Health Check"])
class IsAliveView(APIView):
    """
    Is the application alive?
    """

    serializer_class = IsAliveSerializer

    def get(self, request, *args, **kwargs):
        data = {"is_alive": True}

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

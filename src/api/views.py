from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import GitRefSerializer, IsAliveSerializer

__all__ = (
    "GitRefView",
    "IsAliveView",
)


@extend_schema(tags=["Health Check"])
class GitRefView(APIView):
    """
    Current version of the application
    """

    serializer_class = GitRefSerializer

    def get(self, request, *args, **kwargs):
        data = {
            "branch": settings.GIT_BRANCH,
            "commit_sha": settings.GIT_COMMIT_SHA,
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


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

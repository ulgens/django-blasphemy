from rest_framework.viewsets import ReadOnlyModelViewSet

from ..models import Snippet
from .filters import SnippetFilter
from .serializers import SnippetSerializer

__all__ = ("SnippetViewSet",)


class SnippetViewSet(ReadOnlyModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filterset_class = SnippetFilter

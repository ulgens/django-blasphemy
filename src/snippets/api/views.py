from rest_framework.viewsets import ModelViewSet

from ..models import Snippet  # noqa: TID252
from .filters import SnippetFilter
from .serializers import SnippetSerializer


class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filterset_class = SnippetFilter

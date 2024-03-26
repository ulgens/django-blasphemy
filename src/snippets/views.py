from rest_framework.viewsets import ModelViewSet

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

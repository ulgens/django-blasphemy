from django_filters.rest_framework import FilterSet, filters

from ..choices import LANGUAGE_CHOICES, STYLE_CHOICES
from ..models import Snippet

__all__ = ("SnippetFilter",)


class SnippetFilter(FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    code = filters.CharFilter(lookup_expr="icontains")
    language = filters.ChoiceFilter(choices=LANGUAGE_CHOICES)
    style = filters.ChoiceFilter(choices=STYLE_CHOICES)

    class Meta:
        model = Snippet
        fields = (
            "title",
            "code",
            "language",
            "style",
        )

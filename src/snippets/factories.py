import factory
from factory import fuzzy

from .choices import LANGUAGE_CHOICES, STYLE_CHOICES
from .models import Snippet

LANGUAGE_VALUES = [value for value, _ in LANGUAGE_CHOICES]
STYLE_VALUES = [value for value, _ in STYLE_CHOICES]


class SnippetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Snippet

    title = factory.Faker("sentence")
    code = factory.Faker("text")
    language = fuzzy.FuzzyChoice(LANGUAGE_VALUES)
    style = fuzzy.FuzzyChoice(STYLE_VALUES)

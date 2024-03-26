from django.urls import include, path
from rest_framework.routers import DefaultRouter

from snippets.views import SnippetViewSet

router = DefaultRouter()
router.register("snippets", SnippetViewSet, basename="snippet")

urlpatterns = [
    path("", include(router.urls)),
]

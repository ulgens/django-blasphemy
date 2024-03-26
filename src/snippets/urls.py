from django.urls import include, path
from rest_framework.routers import DefaultRouter

from snippets.views import SnippetViewSet

router = DefaultRouter()
router.register("", SnippetViewSet, basename="snippet")

urlpatterns = [
    path("", include(router.urls)),
]

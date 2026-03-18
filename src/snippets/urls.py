from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import SnippetViewSet

__all__ = ("urlpatterns",)

router = SimpleRouter()
router.register("", SnippetViewSet, basename="snippet")

urlpatterns = [
    path("", include(router.urls)),
]

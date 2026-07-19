from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.reverse import reverse_lazy

from snippets.urls import urlpatterns as snippets_urlpatterns

from .views import GitRefView, IsAliveView

__all__ = ("urlpatterns",)

app_name = "api"
swagger_patterns = [
    path(
        route="openapi.json",
        view=SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        route="docs/",
        view=SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
    path(
        route="",
        view=RedirectView.as_view(url=reverse_lazy("api:swagger-ui")),
        name="home",
    ),
]

urlpatterns = [
    *swagger_patterns,
    path("snippets/", include(snippets_urlpatterns)),
    # Health Check
    path("git_ref/", GitRefView.as_view(), name="git-ref"),
    path("is_alive/", IsAliveView.as_view(), name="is-alive"),
]

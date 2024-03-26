from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.reverse import reverse_lazy
from snippets.urls import urlpatterns as snippets_urlpatterns

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
    ),
]

urlpatterns = [
    *swagger_patterns,
    path("snippets/", include(snippets_urlpatterns)),
]

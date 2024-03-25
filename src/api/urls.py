from django.urls import path, reverse
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.reverse import reverse_lazy

app_name = "api"
urlpatterns = [
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

"""
URL Configuration
"""

from api import urls as api_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

from .views import error, manual_flat_log, manual_log

urlpatterns = [
    path("admin/", admin.site.urls),
    path("error/", error),
    path("manual_log/", manual_log),
    path("manual_flat_log/", manual_flat_log),
    path("api/", include(api_urls)),
    # Don't leave the homepage empty
    path(
        route="",
        view=RedirectView.as_view(url=reverse_lazy("api:home")),
    ),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

"""
URL Configuration
"""

from api import urls as api_urls
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import error, manual_flat_log, manual_log

urlpatterns = [
    path("admin/", admin.site.urls),
    path("error/", error),
    path("manual_log/", manual_log),
    path("manual_flat_log/", manual_flat_log),
    path("api/", include(api_urls)),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

"""
blasphemy URL Configuration

https://docs.djangoproject.com/en/3.2/topics/http/urls/

"""
from django.contrib import admin
from django.urls import path

from .views import error, manual_log, manual_flat_log

urlpatterns = [
    path("admin/", admin.site.urls),
    path("error/", error),
    path("manual_log/", manual_log),
    path("manual_flat_log/", manual_flat_log),
]

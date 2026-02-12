from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self):
        # Register system checks
        from .tests import checks  # noqa: F401

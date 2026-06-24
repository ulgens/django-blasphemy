"""
Sentry setup & settings

https://docs.sentry.io/platforms/python/guides/django/
"""

import logging

import git
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

__all__ = ("init_sentry",)


def init_sentry(env):
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    dsn = env.str("SENTRY_DSN")
    environment = env.str("SENTRY_ENVIRONMENT", default="development")

    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        release=sha,
        # Enabled integrations can be checked via `sentry = sentry_sdk.init(...); sentry._client.integrations`
        # https://docs.sentry.io/platforms/python/configuration/options/#auto-enabling-integrations
        auto_enabling_integrations=True,
        integrations=[
            DjangoIntegration(cache_spans=True),
            LoggingIntegration(event_level=logging.WARNING),
        ],
        send_default_pii=True,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

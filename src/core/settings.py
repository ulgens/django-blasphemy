"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/topics/settings/
"""

# "noqa: ERA001" in this file means the related line added as an example for an alternative
# use case and/or further implementation, and the code should stay there. Think it like a .gitkeep file.
import logging
import sys
from gettext import gettext as _
from pathlib import Path

import environ
from celery.schedules import crontab

# TODO:
#  Compare with dynaconf
#  https://dynaconf.readthedocs.io/en/latest/
env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# FIXME: Read it from the env
# noinspection SpellCheckingInspection
SECRET_KEY = "django-insecure-fwa(zg5eoz9#vogq1$60scfov9o_pj+$kqha-y)#ao0i@g)6@7"  # noqa: S105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definitions
PRIORITY_APPS = [
    "admin_interface",
    "colorfield",
]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INTERNAL_APPS = [
    "core",
    "snippets",
    "users",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "django_filters",
    "django_jsonform",
    "django_migration_vis",
    # TODO: Consider making "django_watchfiles" dev-only
    # TODO: Add benchmark details - reasoning: https://github.com/adamchainz/django-watchfiles/issues/174
    # "django_watchfiles",
    # "drf_spectacular",
    "rest_framework",
]

DEBUG_APPS = [
    "debug_toolbar",
    "django_removals",
]

INSTALLED_APPS = PRIORITY_APPS + DJANGO_APPS + THIRD_PARTY_APPS + INTERNAL_APPS

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#disable-the-toolbar-when-running-tests-optional
TESTING = "test" in sys.argv

if DEBUG and not TESTING:
    INSTALLED_APPS += DEBUG_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG and not TESTING:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    # NonHtmlDebugToolbarMiddleware should be added after DebugToolbarMiddleware
    MIDDLEWARE.append("core.middlewares.NonHtmlDebugToolbarMiddleware")

if not TESTING:
    # Having whitenoise enabled in tests cause
    #    UserWarning: No directory at: /code/src/staticfiles/
    # warning, when we don't even need to serve static files in tests.
    # https://whitenoise.readthedocs.io/en/stable/django.html#enable-whitenoise
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#toolbar-options
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "core.utils.show_debug_toolbar",
    "UPDATE_ON_FETCH": True,
}

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DATABASE_NAME"),
        "USER": env.str("DATABASE_USER"),
        "PASSWORD": env.str("DATABASE_PASSWORD"),
        "HOST": env.str("DATABASE_HOST"),
        "PORT": env.int("DATABASE_PORT"),
    },
}

AUTH_USER_MODEL = "users.User"

SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"user_attributes": ("email", "full_name", "short_name")},
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "mailpit"
EMAIL_PORT = 1025

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGES = (("en", _("English")),)
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# FIXME:
#   Having whitenoise enabled in tests cause
#       ValueError: Missing staticfiles manifest entry for 'admin/css/base.css'
if TESTING:
    STORAGES["staticfiles"] = {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    }


# With the original hashers setting, the test takes ~10x longer.
# https://docs.djangoproject.com/en/5.0/topics/testing/overview/#password-hashing
if TESTING:
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


# Django debug toolbar
if DEBUG:
    import socket

    hostname, aliases, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# Admin related
# https://github.com/fabiocaccamo/django-admin-interface#installation
X_FRAME_OPTIONS = "SAMEORIGIN"
# SILENCED_SYSTEM_CHECKS = ["security.W019"]

# DRF
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.paginations.CursorPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "api.exception_handler.exception_handler",
    # "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Blasphemy",
    "SERVE_INCLUDE_SCHEMA": False,
}

# https://django-filter.readthedocs.io/en/stable/ref/settings.html#filters-verbose-lookups
FILTERS_VERBOSE_LOOKUPS = {
    # Both 'contains' and 'icontains' use the same label in the package's default settings
    # Overriding 'icontains' to have a better distinction between those two lookups
    "icontains": _("contains (case insensitive)"),
}

SHELL_PLUS_IMPORTS = (
    "import wat",
    "from core.tasks import test_task",
    "from users.factories import UserFactory",
    "from snippets.factories import SnippetFactory",
)


GRAPH_MODELS = {
    "app_labels": ("users",),
    "exclude_models": "BaseModel",
    "group_models": True,
    "theme": "original",
}

# FIXME: Get from the env
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND")

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "core.tasks.beat_task",
        "schedule": crontab(minute="*/1"),
    },
}

# Redis
APP_REDIS_URL = env.str("APP_REDIS_URL")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": APP_REDIS_URL,
    },
}

# SSL
# https://stackoverflow.com/a/65934202/1726238
USE_SSL = env.bool("USE_SSL", default=True)
if USE_SSL:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_SCHEME", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Sentry
# https://docs.sentry.io/platforms/python/guides/django/
if env.bool("ENABLE_SENTRY", default=False):
    import git
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        environment=env.str("SENTRY_ENVIRONMENT", "development"),
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

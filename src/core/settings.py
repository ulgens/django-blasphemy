"""
Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/topics/settings/
"""

import os
from pathlib import Path

import dj_database_url
import environ

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
SECRET_KEY = "django-insecure-fwa(zg5eoz9#vogq1$60scfov9o_pj+$kqha-y)#ao0i@g)6@7"  # nosec B105

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
    "users",
]

THIRD_PARTY_APPS = [
    "django_extensions",
]

DEBUG_APPS = [
    "debug_toolbar",
    "django_migrations_formatter.apps.MigrationsFormatter",
]

INSTALLED_APPS = PRIORITY_APPS + DJANGO_APPS + THIRD_PARTY_APPS + INTERNAL_APPS
if DEBUG:
    INSTALLED_APPS += DEBUG_APPS

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


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
DEFAULT_DATABASE_URL = env.str("DATABASE_URL")
DATABASES = {
    "default": dj_database_url.parse(
        DEFAULT_DATABASE_URL,
        conn_max_age=600,
        # ssl_require=True,
    ),
}

AUTH_USER_MODEL = "users.User"


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django debug toolbar
if DEBUG:
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# Admin related
# https://github.com/fabiocaccamo/django-admin-interface#installation
X_FRAME_OPTIONS = "SAMEORIGIN"
# SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Sentry
# https://docs.sentry.io/platforms/python/guides/django/
if env.bool("ENABLE_SENTRY", default=False):
    import logging

    import git
    import sentry_sdk

    # from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    # from sentry_sdk.integrations.redis import RedisIntegration

    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha

    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN"),
        integrations=[
            # CeleryIntegration(),
            DjangoIntegration(),
            # FIXME: Sentry doesn't record info level logs with this config
            LoggingIntegration(level=logging.INFO),
            # RedisIntegration(),
        ],
        environment=env.str("SENTRY_ENVIRONMENT", "development"),
        release=sha,
        send_default_pii=True,
        traces_sample_rate=1.0,
    )

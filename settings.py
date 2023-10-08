import os
import sys
from pathlib import Path

import dj_database_url
import environ

BASE_DIR = Path(__file__).resolve().parent

##########################################################################################
# Environment
# https://django-environ.readthedocs.io/en/latest/quickstart.html
##########################################################################################
env = environ.Env()

# Take environment variables from .env file (if it exists)
# That's why it is important to NOT version .env file
# (otherwise prod environment will get local env file values!)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

ENV_NAME = env("DJ_ENV_NAME")

##########################################################################################
# Security
##########################################################################################

SECRET_KEY = env("DJ_SECRET_KEY")
DEBUG = env("DJ_DEBUG", cast=bool)
CORS_ORIGIN_ALLOW_ALL = True
INTERNAL_IPS = ["127.0.0.1"]  # required for django debug toolbar
ALLOWED_HOSTS = ["*"]  # To edit according your hosting platform
PREFIX_URL_ADMIN = "mason"  # to protect admin page from easy discovery

##########################################################################################
# Apps definition
##########################################################################################

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "django_celery_results",
    "django_celery_beat",
    "django_extensions",  # shell_plus, ...
    "debug_toolbar",
    "phonenumber_field",
]

MY_APPS = ["core", "badges", "profiles"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + MY_APPS

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # to handle CORS with right headers
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "urls"
WSGI_APPLICATION = "wsgi.application"

##########################################################################################
# DX: Adding apps to the path is required for auto import
##########################################################################################

APP_ROOT = "dj_apps"
for new_path in [APP_ROOT] + [f"{APP_ROOT}/{folder}" for folder in MY_APPS]:
    sys.path.insert(0, os.path.join(BASE_DIR, new_path))

##########################################################################################
# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
##########################################################################################

DATABASES = {"default": dj_database_url.config(env="DJ_DATABASE_URL", conn_max_age=600)}

##########################################################################################
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
##########################################################################################

LANGUAGE_CODE = "fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_L10N = True
USE_TZ = True

##########################################################################################
# Templates (required for admin dashboard)
##########################################################################################

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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

##########################################################################################
# Static files
# https://docs.djangoproject.com/en/dev/howto/static-files/
##########################################################################################

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

##########################################################################################
# User related
##########################################################################################
AUTH_USER_MODEL = "profiles.User"

PHONENUMBER_DEFAULT_REGION = "FR"
PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"

##########################################################################################
# Celery
# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html
# https://docs.celeryq.dev/en/stable/userguide/
# tasks execution troubleshooting: https://stackoverflow.com/questions/9769496/celery-received-unregistered-task-of-type-run-example
##########################################################################################

CELERY_BROKER_URL = env("DJ_REDIS_URL")
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-connection-retry-on-startup
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html#django-celery-results-using-the-django-orm-cache-as-a-result-backend
CELERY_RESULT_BACKEND = "django-db"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
CELERY_TASK_SERIALIZER = "json"  # default - change to pickle to serialize complex
# objects
# https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#using-custom-scheduler-classes
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

##########################################################################################
# Misc
##########################################################################################

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

##########################################################################################
# Testing
##########################################################################################

# Used for unit tests and CI to remove logs for example, or deactivate throtling
# https://stackoverflow.com/a/32650980/2255491
if os.environ.get("DJ_TESTING_MODE"):
    TEST_RUNNER = "django_rich.test.RichRunner"
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
    # Celery tasks will be executed locally by blocking until the task returns.
    # Note that the recommendation is to mock instead:
    # https://docs.celeryq.dev/en/stable/userguide/testing.html
    CELERY_TASK_ALWAYS_EAGER = True


##########################################################################################
# Realtime (soketi)
# https://docs.soketi.app/
##########################################################################################
SOKETI_HOST = env("DJ_SOKETI_HOST")
SOKETI_PORT = env("DJ_SOKETI_PORT", cast=int)
SOKETI_APP_ID = env("DJ_SOKETI_APP_ID")
SOKETI_KEY = env("DJ_SOKETI_KEY")
SOKETI_SECRET = env("DJ_SOKETI_SECRET")

import os
import sys
from pathlib import Path

import dj_database_url
import environ
from corsheaders.defaults import default_headers

CONFIG_DIR = Path(__file__).resolve().parent
BASE_DIR = CONFIG_DIR.parent


##########################################################################################
# Environment
# https://django-environ.readthedocs.io/en/latest/quickstart.html
##########################################################################################
env = environ.Env()

# Take environment variables from .env file (if it exists)
# That's why it is important to NOT version .env file
# (otherwise prod environment will get local env file values!)
environ.Env.read_env(os.path.join(CONFIG_DIR, ".env"))

ENV_NAME = env("DJ_ENV_NAME")

##########################################################################################
# Security
##########################################################################################

SECRET_KEY = env("DJ_SECRET_KEY")
DEBUG = env("DJ_DEBUG", cast=bool)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + ("x-api-key",)  # required for django-ninja
INTERNAL_IPS = ["127.0.0.1"]  # required for django debug toolbar
ALLOWED_HOSTS = ["*"]  # To edit according your hosting platform
PREFIX_URL_ADMIN = "mason"  # to protect admin page from easy discovery

##########################################################################################
# Apps definition
# My apps are automatically generated based on the filesystem
# Then added to the path for auto import
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
    "safedelete",
    "django_celery_results",
    "django_celery_beat",
    "django_extensions",  # shell_plus, ...
    "debug_toolbar",
    "phonenumber_field",
]

APP_FOLDER = "dj_apps"

MY_APPS = os.listdir(BASE_DIR / Path(APP_FOLDER))


for new_path in [APP_FOLDER] + [f"{APP_FOLDER}/{folder}" for folder in MY_APPS]:
    sys.path.insert(0, os.path.join(BASE_DIR, new_path))

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
WSGI_APPLICATION = "config.wsgi.application"


##########################################################################################
# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
##########################################################################################

DATABASES = {"default": dj_database_url.config(env="DJ_DATABASE_URL", conn_max_age=600)}

##########################################################################################
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
##########################################################################################

LANGUAGE_CODE = "en"
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
# Realtime (soketi)
# https://docs.soketi.app/
##########################################################################################
SOKETI_HOST = env("DJ_SOKETI_HOST")
SOKETI_PORT = env("DJ_SOKETI_PORT", cast=int)
SOKETI_APP_ID = env("DJ_SOKETI_APP_ID")
SOKETI_KEY = env("DJ_SOKETI_KEY")
SOKETI_SECRET = env("DJ_SOKETI_SECRET")

##########################################################################################
# Mailing
# https://docs.djangoproject.com/en/dev/topics/email/#email-backends
##########################################################################################

EMAIL_BACKEND_SLUG = env("DJ_EMAIL_BACKEND_SLUG")
EMAIL_BACKEND = f"django.core.mail.backends.{EMAIL_BACKEND_SLUG}.EmailBackend"
if EMAIL_BACKEND_SLUG == "smtp":
    EMAIL_HOST = env("DJ_EMAIL_HOST")
    EMAIL_HOST_USER = env("DJ_EMAIL_API_TOKEN")
    EMAIL_HOST_PASSWORD = env("DJ_EMAIL_API_TOKEN")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

##########################################################################################
# Media files / Object storage
##########################################################################################

# TODO: new 4.2 storage variables:
# https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STORAGES

# USE_SPACES = env("DJ_USE_SPACES", cast=bool)

# if USE_SPACES is True:
#     # s3 settings
#     AWS_ACCESS_KEY_ID = env("DJ_AWS_ACCESS_KEY_ID")
#     AWS_SECRET_ACCESS_KEY = env("DJ_AWS_SECRET_ACCESS_KEY")
#     AWS_STORAGE_BUCKET_NAME = env("DJ_AWS_STORAGE_BUCKET_NAME")
#     AWS_DEFAULT_ACL = "public-read"
#     AWS_S3_ENDPOINT_URL = "https://fra1.digitaloceanspaces.com"
#     AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
#     # media settings
#     MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/media/"
#     DEFAULT_FILE_STORAGE = "dj_config.storage_backends.PublicMediaStorage"
# else:
#     MEDIA_URL = "/media/"
#     MEDIA_ROOT = BASE_DIR / "mediafiles"
#     DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

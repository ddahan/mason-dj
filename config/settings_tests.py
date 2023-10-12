from .settings import *  # noqa

# Speed tests up a lot
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# Celery tasks will be executed locally by blocking until the task returns.
# Note that the recommendation is to mock instead:
# https://docs.celeryq.dev/en/stable/userguide/testing.html
CELERY_TASK_ALWAYS_EAGER = True

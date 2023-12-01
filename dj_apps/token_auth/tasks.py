from config.celery import app

from .models.api_token import APIAccessToken
from .models.password_less_token import LoginPasswordLessToken, SignupPasswordLessToken


@app.task()
def delete_expired_tokens():
    APIAccessToken.objects.expired().delete()
    SignupPasswordLessToken.objects.expired().delete()
    LoginPasswordLessToken.objects.expired().delete()

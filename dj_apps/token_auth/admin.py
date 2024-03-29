from django.contrib import admin

from .models.api_token import APIAccessToken
from .models.magic_link_token import MagicLinkToken
from .models.password_less_token import LoginPasswordLessToken, SignupPasswordLessToken


@admin.register(APIAccessToken)
class APIAccessTokenAdmin(admin.ModelAdmin):
    list_display = ("expiration", "key", "user")
    list_filter = ("expiration", "user")


@admin.register(MagicLinkToken)
class MagicLinkTokenAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "modified",
        "expiration",
        "key",
        "user",
        "usage",
    )
    list_filter = ("expiration", "user")


@admin.register(LoginPasswordLessToken)
class LoginPasswordLessTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sid",
        "created",
        "modified",
        "expiration",
        "key",
        "user",
    )
    list_filter = ("expiration", "user")


@admin.register(SignupPasswordLessToken)
class SignupPasswordLessTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sid",
        "created",
        "modified",
        "expiration",
        "key",
        "email",
    )
    list_filter = ("expiration",)

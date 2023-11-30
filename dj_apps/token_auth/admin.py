from django.contrib import admin

from .models.api_token import APIToken
from .models.magic_link_token import MagicLinkToken
from .models.password_less_token import LoginPasswordLessToken, SignupPasswordLessToken


@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ("created", "modified", "key", "user")
    list_filter = ("created", "modified", "user")


@admin.register(MagicLinkToken)
class MagicLinkTokenAdmin(admin.ModelAdmin):
    list_display = (
        "created",
        "modified",
        "key",
        "end_of_validity",
        "user",
        "usage",
    )
    list_filter = ("created", "modified", "end_of_validity", "user")


@admin.register(LoginPasswordLessToken)
class LoginPasswordLessTokenAdmin(admin.ModelAdmin):
    list_display = (
        "end_of_validity",
        "key",
        "user",
    )
    list_filter = ("created", "modified", "end_of_validity", "user")


@admin.register(SignupPasswordLessToken)
class SignupPasswordLessTokenAdmin(admin.ModelAdmin):
    list_display = (
        "end_of_validity",
        "key",
        "email",
    )
    list_filter = ("created", "modified", "end_of_validity", "email")

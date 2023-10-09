from django.contrib import admin

from .models.api_token import APIToken
from .models.magic_link_token import MagicLinkToken
from .models.password_less_token import PasswordLessToken

admin.site.register((APIToken, PasswordLessToken, MagicLinkToken))

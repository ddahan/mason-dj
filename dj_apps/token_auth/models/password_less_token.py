from datetime import timedelta as td

from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.manager import Manager

from core.mixins.secret_id import SecretID
from mailing.models.mail_skeleton import MailSkeleton

from ..mixins.consumable import ConsumableMixin
from ..mixins.digit_6_key import Digit6KeyMixin
from ..mixins.endable import EndableMixin, EndableMixinQuerySet
from .base_token import BaseToken


class PasswordLessTokenQuerySet(EndableMixinQuerySet):
    pass


class BasePasswordLessToken(
    SecretID, Digit6KeyMixin, EndableMixin, ConsumableMixin, BaseToken
):
    """
    6-digit token received  to validate identity. Many tokens with the same key can co-exist.
    """

    objects = Manager.from_queryset(PasswordLessTokenQuerySet)()

    VALIDITY_TIME = td(minutes=20)

    @classmethod
    def challenge(cls, input_code, user) -> bool:
        """Return True if the challenge is successful after consuming the token,
        False otherwise."""

        # Technically, there could be multiple tokens with the same code for a single user
        valid_tokens = cls.objects.valids_for_user(user).filter(key=input_code)
        if valid_tokens.exists():
            token_to_consume = valid_tokens[0]
            token_to_consume.consume()
            return True

        return False


class LoginPasswordLessToken(BasePasswordLessToken):
    class Meta:
        db_table = "tb_login_password_less_tokens"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="passwordless_tokens",
        verbose_name="utilisateur",
    )

    @classmethod
    def send_new_to(cls, user):
        new_token = cls.objects.create(user=user)
        MailSkeleton.send_with(
            "SEND_LOGIN_PASSWORDLESS_CODE", {user.email: {"code": new_token.key}}
        )


class SignupPasswordLessToken(BasePasswordLessToken):
    class Meta:
        db_table = "tb_signup_password_less_tokens"

    email = models.EmailField()

    @classmethod
    def send_new_to(cls, email: str):
        new_token = cls.objects.create(email=email)
        MailSkeleton.send_with(
            "SEND_SIGNUP_PASSWORDLESS_CODE", {email: {"code": new_token.key}}
        )

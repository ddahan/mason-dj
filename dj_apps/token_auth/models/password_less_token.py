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
    SecretID,
    Digit6KeyMixin,
    EndableMixin,
    ConsumableMixin,
    BaseToken,
):
    """
    6-digit token received to validate identity. Many tokens with the same key can co-exist.
    """

    class Meta:
        abstract = True

    objects = Manager.from_queryset(PasswordLessTokenQuerySet)()

    VALIDITY_TIME = td(minutes=20)

    @classmethod
    def challenge(cls, input_code, filtering: dict, consume=True) -> bool:
        """
        Generic challenge method. 'filtering' is a dictionary that specifies
        additional filtering criteria for the valid tokens, to be used by children methods.
        """
        valid_tokens = cls.objects.filter(key=input_code, **filtering)
        if valid_tokens.exists():
            token = valid_tokens[0]
            if consume:
                token.consume()
            return True

        return False


class LoginPasswordLessToken(
    SecretID, Digit6KeyMixin, EndableMixin, ConsumableMixin, BaseToken
):
    class Meta:
        db_table = "tb_login_password_less_tokens"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="passwordless_tokens",
        verbose_name="utilisateur",
    )

    @classmethod
    def challenge(cls, input_code, user) -> bool:
        """Specific challenge logic for LoginPasswordLessToken."""
        return super().challenge(input_code, {"user": user})

    @classmethod
    def send_new_to(cls, user):
        new_token = cls.objects.create(user=user)
        MailSkeleton.send_with(
            "SEND_LOGIN_PASSWORDLESS_CODE", {user.email: {"code": new_token.key}}
        )


class SignupPasswordLessToken(
    SecretID, Digit6KeyMixin, EndableMixin, ConsumableMixin, BaseToken
):
    class Meta:
        db_table = "tb_signup_password_less_tokens"

    email = models.EmailField()

    @classmethod
    def challenge(cls, input_code, email, consume=True) -> bool:
        """Specific challenge logic for SignupPasswordLessToken."""
        return super().challenge(input_code, {"email": email}, consume)

    @classmethod
    def send_new_to(cls, email: str):
        new_token = cls.objects.create(email=email)
        MailSkeleton.send_with(
            "SEND_SIGNUP_PASSWORDLESS_CODE", {email: {"code": new_token.key}}
        )

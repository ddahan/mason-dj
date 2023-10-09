from datetime import timedelta as td

from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.manager import Manager

from core.mixins.secret_id import SecretID

from ..mixins.consumable import ConsumableMixin
from ..mixins.digit_6_key import Digit6KeyMixin
from ..mixins.endable import EndableMixin, EndableMixinQuerySet
from .base_token import BaseToken


class PasswordLessTokenQuerySet(EndableMixinQuerySet):
    pass


class PasswordLessToken(
    SecretID, Digit6KeyMixin, EndableMixin, ConsumableMixin, BaseToken
):
    """
    6-digit token received by a user to validate its identity when signin or signup.
    Many tokens with the same key can co-exist.
    """

    objects = Manager.from_queryset(PasswordLessTokenQuerySet)()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="passwordless_tokens"
    )

    VALIDITY_TIME = td(minutes=20)

    class Meta:
        db_table = "tb_password_less_tokens"

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

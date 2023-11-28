from datetime import timedelta as td
from posixpath import join
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.manager import Manager

from core.mixins.auto_validable import AutoValidable

from ..mixins.consumable import ConsumableMixin
from ..mixins.endable import EndableMixin, EndableMixinQuerySet
from ..mixins.unique_secret_key import UniqueSecretKeyMixin
from .base_token import BaseToken


class MagicLinkUsage(models.TextChoices):
    RESET_PASSWORD = "reset-password", "Reset Password"
    # SIGNUP = "signup", "Sign up"
    # LOGIN = "login", "Log in"


class MagicLinkTokenQuerySet(EndableMixinQuerySet):
    pass


class MagicLinkToken(
    UniqueSecretKeyMixin, EndableMixin, ConsumableMixin, BaseToken, AutoValidable
):
    """
    Token received by a user to validate its email
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="magiclink_tokens",
        verbose_name="utilisateur",
    )
    usage = models.CharField(max_length=1024, choices=MagicLinkUsage.choices)

    class Meta:
        db_table = "tb_magic_link_tokens"

    VALIDITY_TIME = td(days=1)

    objects = Manager.from_queryset(MagicLinkTokenQuerySet)()

    @property
    def as_front_url(self) -> str:
        """
        Build a magic link url to be used with any an external front-end app
        """
        return join(
            settings.FRONT_HOST,
            settings.FRONT_ROUTE_USE_MAGIC_LINK,
            self.usage.value,
            self.key,
        )

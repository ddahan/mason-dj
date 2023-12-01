from datetime import timedelta as td
from posixpath import join
from urllib.parse import urlencode

from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.manager import Manager

from core.mixins.auto_validable import AutoValidable
from mailing.models.mail_skeleton import MailSkeleton

from ..mixins.consumable import ConsumableMixin
from ..mixins.expirable import ExpirableMixin, ExpirableMixinQuerySet
from ..mixins.unique_secret_key import UniqueSecretKeyMixin
from .base_token import BaseToken


class MagicLinkUsage(models.TextChoices):
    """Usage value is the front-url to access"""

    RESET_PASSWORD = "auth/classic/reset-password", "Reset Password"


class MagicLinkTokenQuerySet(ExpirableMixinQuerySet):
    pass


class MagicLinkToken(
    UniqueSecretKeyMixin, ExpirableMixin, ConsumableMixin, BaseToken, AutoValidable
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

    def as_front_url(self, **query_params) -> str:
        """
        Build a magic link url to be used with any an external front-end app
        """
        base_url = join(settings.FRONT_HOST, self.usage.value)
        return f"{base_url}?{urlencode(query_params)}"

    @classmethod
    def send_new_to(cls, user, usage: MagicLinkUsage.choices):
        new_token = cls.objects.create(user=user, usage=usage)
        MailSkeleton.send_with(
            "SEND_RESET_PASSWORD_LINK",
            {user.email: {"magic_link": new_token.as_front_url(key=new_token.key)}},
        )

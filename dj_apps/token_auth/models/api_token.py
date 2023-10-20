from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE

from ..mixins.revocable import RevocableMixin
from ..mixins.unique_secret_key import UniqueSecretKeyMixin
from .base_token import BaseToken


class APIToken(UniqueSecretKeyMixin, RevocableMixin, BaseToken):
    """
    Token used by user to access programming API, develired after a successful login
    """

    class Meta:
        db_table = "tb_api_tokens"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="api_token",
        verbose_name="utilisateur",
    )

    def __str__(self):
        return f"{self.user} 🔑 {self.key}"

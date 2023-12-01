from __future__ import annotations

from datetime import timedelta as td

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

from ..mixins.expirable import ExpirableMixin, ExpirableMixinQuerySet
from ..mixins.revocable import RevocableMixin
from ..mixins.unique_secret_key import UniqueSecretKeyMixin
from .base_token import BaseToken

User = get_user_model()


class APIAccessTokenQuerySet(ExpirableMixinQuerySet):
    pass


class APIAccessToken(UniqueSecretKeyMixin, ExpirableMixin, RevocableMixin, BaseToken):
    """
    Token to access programming API, develired after a successful login.
    It will be stored on front-end (e.g. in local storage).
    """

    class Meta:
        db_table = "tb_api_access_tokens"

    objects = models.Manager.from_queryset(APIAccessTokenQuerySet)()
    VALIDITY_TIME = td(weeks=1)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="api_access_tokens"
    )

    def __str__(self):
        return f"{self.user} 🔑 {self.key}"

    @classmethod
    def challenge(cls, key) -> User | None:
        """Try to get a User object from the token key.
        This is used everytime the front-end is passing a token key in a request which requires authentication.
        """
        try:
            token = cls.objects.unexpired().get(key=key)
        except cls.DoesNotExist:
            return None
        else:
            return token.user

import secrets

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UniqueSecretKeyMixin(models.Model):
    class Meta:
        abstract = True

    """Add fields and features related to a unique key generated """

    key = models.CharField(primary_key=True, max_length=512, unique=True, editable=False)

    def _build_key(self) -> str:
        return secrets.token_urlsafe(32)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.key = self._build_key()
        super().save(*args, **kwargs)

    @classmethod
    def try_get_user_from_token(cls, input_key) -> User | None:
        """key must be unique sothat it works."""
        try:
            token = cls.objects.get(key=input_key)
        except cls.DoesNotExist:
            return None
        else:
            return token.user

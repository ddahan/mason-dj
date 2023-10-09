from django.db import models


class RevocableMixin(models.Model):
    """Add the ability to revoque a token. Currently, revocating the token is
    equivalent to hard deleting it."""

    class Meta:
        abstract = True

    def revoque(self):
        self.delete()

    @classmethod
    def revoque_all_for_user(cls, user) -> None:
        for token in cls.objects.filter(user=user):
            token.revoque()

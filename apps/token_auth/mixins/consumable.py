from django.db import models


class ConsumableMixin(models.Model):
    """Add the ability to consume a token. Currently, consuming the token is
    equivalent to hard deleting it."""

    class Meta:
        abstract = True

    def consume(self):
        self.delete()

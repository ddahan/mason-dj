from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import query
from django.utils import timezone


class ExpirableMixinQuerySet(query.QuerySet):
    def unexpired(self):
        now = timezone.now()
        return self.filter(expiration__gte=now)

    def expired(self):
        now = timezone.now()
        return self.filter(expiration__lt=now)


class ExpirableMixin(models.Model):
    """Add fields and end of validity feature to a token"""

    class Meta:
        abstract = True

    expiration = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not hasattr(self, "VALIDITY_TIME"):
            raise ImproperlyConfigured("VALIDITY_TIME attribute must be defined")
        if self._state.adding:
            self.expiration = timezone.now() + self.VALIDITY_TIME
        super().save(*args, **kwargs)

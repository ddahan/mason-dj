from django.db import models
from django.utils.timezone import is_naive, make_aware, now


class ExpirableQueryset(models.query.QuerySet):
    def expired(self):
        return self.filter(expiration__lte=now())

    def unexpired(self):
        return self.filter(expiration__gt=now())


class Expirable(models.Model):
    """Add an optionnal expiration datetime"""

    class Meta:
        abstract = True

    expiration = models.DateTimeField(blank=True, null=True)

    @property
    def expired(self) -> bool:
        return bool(self.expiration and now() > self.expiration)

    def save(self, *args, **kwargs):
        if self.expiration and is_naive(self.expiration):
            make_aware(self.expiration)
        super().save(*args, **kwargs)

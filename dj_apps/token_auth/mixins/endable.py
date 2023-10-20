from django.db import models
from django.db.models import query
from django.utils import timezone


class EndableMixinQuerySet(query.QuerySet):
    def valids(self):
        now = timezone.now()
        return self.filter(end_of_validity__gte=now)

    def valids_for_user(self, user):
        return self.valids().filter(user=user)

    def invalids(self):
        now = timezone.now()
        return self.filter(end_of_validity__lt=now)


class EndableMixin(models.Model):
    """Add fields and end of validity feature to a token"""

    class Meta:
        abstract = True

    end_of_validity = models.DateTimeField(verbose_name="fin de validité")

    def save(self, *args, **kwargs):
        if not hasattr(self, "VALIDITY_TIME"):
            raise NotImplementedError("VALIDITY_TIME attribute must be defined")
        if self._state.adding:
            self.end_of_validity = timezone.now() + self.VALIDITY_TIME
        super().save(*args, **kwargs)

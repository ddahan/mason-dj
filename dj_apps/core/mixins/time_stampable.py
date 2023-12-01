from django.db import models
from django.utils import timezone


class TimeStampableQueryset(models.query.QuerySet):
    class Meta:
        abstract = True

    def created_between(self, i_start, i_end):
        """
        Returns all objects created between the provided interval
        """

        assert i_start <= i_end
        return self.filter(created__lte=i_end, created__gte=i_start)


class TimeStampable(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """
        We don't use auto_now nor auto_now_add as this prevent to get the exact same
        value for created and modified fields.
        """
        now = timezone.now()
        if self._state.adding:
            self.created = now
        self.modified = now

        super().save(*args, **kwargs)

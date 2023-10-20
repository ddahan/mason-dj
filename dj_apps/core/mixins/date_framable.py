from django.db import models

from ..exceptions import InconsistencyException


class DateFramable(models.Model):
    class Meta:
        abstract = True

    start = models.DateField(verbose_name="début")
    end = models.DateField(verbose_name="fin")

    def save(self, *args, **kwargs):
        if self.end < self.start:
            raise InconsistencyException
        super().save()

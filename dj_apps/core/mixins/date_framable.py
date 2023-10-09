from django.db import models

from ..exceptions import InconsistencyException


class DateFramable(models.Model):
    class Meta:
        abstract = True

    start = models.DateField()
    end = models.DateField()

    def save(self, *args, **kwargs):
        if self.end < self.start:
            raise InconsistencyException
        super().save()

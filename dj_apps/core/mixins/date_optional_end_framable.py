from django.db import models


class TimeIconsistencyException(ValueError):
    pass


class DateOptionalEndFramable(models.Model):
    class Meta:
        abstract = True

    start = models.DateField(verbose_name="début")
    end = models.DateField(blank=True, null=True, verbose_name="fin")

    def save(self, *args, **kwargs):
        if self.end:
            if self.end < self.start:
                raise TimeIconsistencyException
        super().save()

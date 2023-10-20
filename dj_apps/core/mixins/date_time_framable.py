from datetime import date

from django.db import models
from django.utils import timezone

from .common.framable import Framable, FramableQueryset


class DateTimeFramableQuerySet(FramableQueryset, models.query.QuerySet):
    class Meta:
        abstract = True

    def in_frame(self):
        """Returns all objects that have an intersection with now"""
        now = timezone.now()
        return self.filter(start__lte=now, end__gte=now)

    def before_frame(self):
        """Returns all objects that are before now"""
        now = timezone.now()
        return self.filter(end__lte=now)

    def after_frame(self):
        """Returns all objects that are after now"""
        now = timezone.now()
        return self.filter(start__gte=now)

    def day(self, day: date = None):
        """Return all objects that starts the provided day"""
        return self.filter(start__date=day)

    def today(self):
        """Return all objects that starts today"""
        today = timezone.now().today().date()
        return self.filter(start__date=today)


class DateTimeFramable(Framable, models.Model):
    class Meta:
        abstract = True

    start = models.DateTimeField(verbose_name="début")
    end = models.DateTimeField(verbose_name="fin")

    @property
    def is_current(self):
        return self.start < timezone.now() < self.end

    @property
    def is_before(self):
        return timezone.now() < self.start

    @property
    def is_after(self):
        return timezone.now() > self.end

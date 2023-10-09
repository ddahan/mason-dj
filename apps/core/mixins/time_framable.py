from django.db import models
from django.utils.timezone import make_naive, now

from .common.framable import Framable, FramableQueryset


class TimeFramableQuerySet(FramableQueryset, models.query.QuerySet):
    class Meta:
        abstract = True

    def in_frame(self):
        """Returns all objects that have an intersection with current time"""
        time_now = make_naive(now()).time()
        return self.filter(start__lte=time_now, end__gte=time_now)


class TimeFramable(Framable, models.Model):
    class Meta:
        abstract = True

    start = models.TimeField()
    end = models.TimeField()

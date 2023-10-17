from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.query_utils import Q


class FramableQueryset(models.query.QuerySet):
    class Meta:
        abstract = True

    def in_interval(self, i_start, i_end):
        """
        Returns all objects whose interval has an intersection with the provided interval
        """

        return self.filter(
            (
                # condition1: any overlap between frames
                Q(start__lte=i_start, end__gte=i_start)
                | Q(start__lte=i_end, end__gte=i_end)
                | Q(start__gte=i_start, start__lte=i_end)
                | Q(end__gte=i_start, end__lte=i_end)
            ),
            # condition2: no same borders
            ~Q(end=i_start) & ~Q(start=i_end),
        )


class Framable(models.Model):
    class Meta:
        abstract = True

    def _check_start_end(self):
        """Raises a ValidationError if end is not after start"""

        if self.end:
            if self.start >= self.end:
                raise ValidationError("End date must be after begin date.")

    def clean(self):
        self._check_start_end()

    @staticmethod
    def has_intersection(p1, p2):
        """Return True if 2 framed elements have an intersection"""

        # condition1: any overlap between frames
        condition_1 = (
            p2.start <= p1.start <= p2.end
            or p2.start <= p1.end <= p2.end
            or p1.start <= p2.start <= p1.end
            or p1.start <= p2.end <= p1.end
        )

        # condition2: no same borders
        condition_2 = p1.start != p2.end and p1.end != p2.start

        return condition_1 and condition_2

from django.db import models


class Singletonable(models.Model):
    """
    This class can be instanciated only once and not deleted.
    It's not exactly the singleton behaviour, but matches what we need.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

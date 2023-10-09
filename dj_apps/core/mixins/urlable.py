from django.db import models


class Urlable(models.Model):
    class Meta:
        abstract = True

    url = models.CharField(max_length=512)

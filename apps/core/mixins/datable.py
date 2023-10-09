from django.db import models


class Datable(models.Model):
    class Meta:
        abstract = True

    date = models.DateField()

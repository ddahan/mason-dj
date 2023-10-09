from django.db import models


class Descriptable(models.Model):
    class Meta:
        abstract = True

    description = models.TextField(blank=True, null=False)

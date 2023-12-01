from django.db import models


class ImagePathable(models.Model):
    class Meta:
        abstract = True

    image_path = models.CharField(max_length=512)


class OptionalImagePathable(models.Model):
    class Meta:
        abstract = True

    image_path = models.CharField(max_length=512, blank=True, null=False)

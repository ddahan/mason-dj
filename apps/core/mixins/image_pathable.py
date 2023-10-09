from django.db import models


class InvertableOnDark(models.Model):
    class Meta:
        abstract = True

    invert_on_dark = models.BooleanField(default=False)


class ImagePathable(InvertableOnDark, models.Model):
    class Meta:
        abstract = True

    image_path = models.CharField(max_length=512)


class OptionalImagePathable(InvertableOnDark, models.Model):
    class Meta:
        abstract = True

    image_path = models.CharField(max_length=512, blank=True, null=False)

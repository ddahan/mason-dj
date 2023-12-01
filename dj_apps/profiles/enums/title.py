from django.db import models


class Title(models.TextChoices):
    MISS = "MISS", "Miss"
    MRS = "MRS", "Mrs."
    MR = "MR", "Mr."

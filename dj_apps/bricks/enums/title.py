from django.db import models


class Title(models.TextChoices):
    MLLE = "MLLE", "mademoiselle"
    MME = "MME", "madame"
    M = "M", "monsieur"

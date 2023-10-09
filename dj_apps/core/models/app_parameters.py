from django.db import models

from mixins.singletonable import Singletonable


class AppParameters(Singletonable, models.Model):
    """
    This class contains all the applicative parameters.
    It must be a singleton and must be created before all other classes, because other
    classes will use these singleton instance to be filled themselves.
    """

    class Meta:
        db_table = "tb_app_parameters"
        verbose_name_plural = "App parameters"

    CONTACT_EMAIL = models.CharField(help_text="Adresse e-mail de contact par défaut")

    def __str__(self):
        return "AppParameters Singleton Object"

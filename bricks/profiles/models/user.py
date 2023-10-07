from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from enums.title import Title
from mixins.auto_validable import AutoValidable
from mixins.deactivable import Deactivable
from phonenumber_field.modelfields import PhoneNumberField

from ...core.models.base_model import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Custom User Manager is required when defining a custom User class"""

        user = self.model(
            email=email,
            is_superuser=False,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(Deactivable, AutoValidable, PermissionsMixin, AbstractBaseUser, BaseModel):
    class Meta:
        verbose_name = "utilisateur"
        ordering = ["-created"]
        get_latest_by = "created"

    email = models.EmailField("e-mail", unique=True)
    title = models.CharField("civilité", choices=Title.choices, max_length=128)
    first_name = models.CharField("prénom", max_length=150)
    last_name = models.CharField("nom", max_length=150)
    phone_number = PhoneNumberField("téléphone", blank=True, null=True)
    birth_date = models.DateField("date de naissance", blank=True, null=True)
    is_staff = models.BooleanField("staff ?", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"  # 🔗 https://bit.ly/3w1KadY
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "title",
    ]  # 🔗 https://bit.ly/3dknLlD

    def clean(self) -> None:
        # NOTE: full_clean() is called in save() with the Autovalidable mixin
        self.email = self.email.lower()
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.upper()

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def small_name(self) -> str:
        return f"{self.first_name[0]}. {self.last_name}"

    def __str__(self):
        return self.name

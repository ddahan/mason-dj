from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models, transaction

from phonenumber_field.modelfields import PhoneNumberField

from core.mixins.auto_validable import AutoValidable
from core.mixins.deactivable import Deactivable
from core.mixins.secret_id import SecretID
from core.mixins.time_stampable import TimeStampable

from ..enums.title import Title


class UserManager(BaseUserManager):
    @transaction.atomic()
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


class User(
    Deactivable,
    PermissionsMixin,
    AbstractBaseUser,
    AutoValidable,
    SecretID,
    TimeStampable,
):
    class Meta:
        db_table = "tb_users"
        ordering = ["-created"]
        get_latest_by = "created"

    email = models.EmailField(unique=True)
    title = models.CharField(choices=Title.choices)
    first_name = models.CharField()
    last_name = models.CharField()
    phone_number = PhoneNumberField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)

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

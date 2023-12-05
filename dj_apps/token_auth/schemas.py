from django.contrib.auth import get_user_model

from ninja import ModelSchema, Schema
from pydantic import validator

User = get_user_model()


class UserSchemaInCreate(ModelSchema):
    class Meta:
        model = User
        fields = ("title", "first_name", "last_name", "email", "password")
        extra = "forbid"


class UserSchemaInLogin(Schema):
    email: str
    password: str

    @validator("email")
    def normalize_email(cls, value):
        """Normalize the email address to lowercase. This is not required for signup as it is done at Django validation level."""
        return value.lower()


class UserSchemaOut(Schema):
    sid: str
    email: str
    api_token_key: str


class UserProfileOut(ModelSchema):
    class Meta:
        model = User
        fields = ("sid", "email")


class EmailSchemaIn(Schema):
    email: str

    @validator("email")
    def normalize_email(cls, value):
        """Normalize the email address to lowercase. This is not required for signup as it is done at Django validation level."""
        return value.lower()


class EnterVerificationCodeSchemaIn(Schema):
    email: str
    code: str  # no need to add extra validation here


class ResetPasswordSchemaIn(Schema):
    key: str
    new_password: str

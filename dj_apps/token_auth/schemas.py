from django.contrib.auth import get_user_model

from ninja import ModelSchema, Schema

User = get_user_model()


class UserSchemaInCreate(ModelSchema):
    class Meta:
        model = User
        fields = ("title", "first_name", "last_name", "email", "password")
        extra = "forbid"


class UserSchemaInLogin(ModelSchema):
    class Meta:
        model = User
        fields = ("email", "password")
        extra = "forbid"


class UserSchemaOut(ModelSchema):
    class Meta:
        model = User
        fields = ("sid", "email")

    api_token_key: str


class EmailSchemaIn(Schema):
    email: str  # we could use EmailStr


class EnterVerificationCodeSchemaIn(Schema):
    email: str
    code: str  # no need to add extra validation here


class ResetPasswordSchemaIn(Schema):
    key: str
    new_password: str

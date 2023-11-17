from django.contrib.auth import get_user_model

from ninja import ModelSchema

User = get_user_model()


class UserSchemaInCreate(ModelSchema):
    class Config:
        model = User
        model_fields = ("title", "first_name", "last_name", "email", "password")
        extra = "forbid"


class UserSchemaOut(ModelSchema):
    class Config:
        model = User
        model_fields = ("sid", "email")

from django.contrib.auth import get_user_model

from ninja import ModelSchema

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


class EmailSchemaIn(ModelSchema):
    class Meta:
        model = User
        fields = ("email",)
        extra = "forbid"

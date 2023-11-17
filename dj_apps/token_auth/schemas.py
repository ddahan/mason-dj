from django.contrib.auth import get_user_model

from ninja import ModelSchema

User = get_user_model()


class UserSchemaInCreate(ModelSchema):
    class Meta:
        model = User
        fields = ("title", "first_name", "last_name", "email", "password")
        extra = "forbid"


class UserSchemaOut(ModelSchema):
    class Meta:
        model = User
        fields = ("sid", "email")
from django.contrib.auth import get_user_model

from ninja import ModelSchema

User = get_user_model()


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ("id", "email")

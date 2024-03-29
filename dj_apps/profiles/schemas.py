from django.contrib.auth import get_user_model

from ninja import Field, ModelSchema

User = get_user_model()


class OwnerBadgeSchemaOut(ModelSchema):
    label: str = Field(None, alias="name")

    class Meta:
        model = User
        fields = ("id",)

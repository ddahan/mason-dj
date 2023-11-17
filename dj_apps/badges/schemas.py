from ninja import ModelSchema, Schema

from profiles.schemas import UserSchema

from .models import Badge


class BadgeSchemaOut(ModelSchema):
    owner: UserSchema

    class Meta:
        model = Badge
        fields = ("identifier", "expiration", "is_active")


class BadgeSchemaInCreate(ModelSchema):
    class Meta:
        model = Badge
        fields = ("identifier", "expiration", "is_active")
        extra = "forbid"


class BadgeSchemaInUpdate(ModelSchema):
    class Meta:
        model = Badge
        fields = ("expiration", "is_active")
        fields_optional = ("expiration", "is_active")

    class Config(Schema.Config):
        extra = "forbid"

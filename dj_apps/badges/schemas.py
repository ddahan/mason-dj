from ninja import ModelSchema

from profiles.endpoints import UserSchema

from .models import Badge


class BadgeSchemaOut(ModelSchema):
    owner = UserSchema

    class Config:
        model = Badge
        model_fields = ("sid", "expiration", "is_active")


class BadgeSchemaInCreate(ModelSchema):
    class Config:
        model = Badge
        model_fields = ("expiration",)


class BadgeSchemaInUpdate(ModelSchema):
    class Config:
        model = Badge
        model_fields = ("expiration", "is_active")

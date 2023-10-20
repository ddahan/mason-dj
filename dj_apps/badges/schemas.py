from ninja import ModelSchema

from profiles.schemas import UserSchema

from .models import Badge


class BadgeSchemaOut(ModelSchema):
    owner = UserSchema

    class Config:
        model = Badge
        model_fields = ("identifier", "expiration", "is_active")


class BadgeSchemaInCreate(ModelSchema):
    class Config:
        model = Badge
        model_fields = ("identifier", "expiration", "is_active")
        extra = "forbid"


class BadgeSchemaInUpdate(ModelSchema):
    class Config:
        model = Badge
        model_fields = ("expiration", "is_active")
        model_fields_optional = ("expiration", "is_active")
        extra = "forbid"

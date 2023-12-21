from ninja import Field, ModelSchema

from profiles.schemas import OwnerBadgeSchemaOut

from .models import Badge


class BadgeSchemaOut(ModelSchema):
    owner: OwnerBadgeSchemaOut
    expired: bool = Field(None, alias="expired")

    class Meta:
        model = Badge
        fields = ("identifier", "expiration", "is_active")


class BadgeSchemaIn(ModelSchema):
    owner_sid: str

    class Meta:
        model = Badge
        fields = ("expiration", "is_active")
        fields_optional = ("expiration", "is_active")

    model_config = {"extra": "forbid"}

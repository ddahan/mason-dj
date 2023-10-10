from django.shortcuts import get_object_or_404

from ninja import ModelSchema, Router

from profiles.endpoints import UserSchema

from .models.badge import Badge

router = Router()


class BadgeSchema(ModelSchema):
    owner: UserSchema

    class Config:
        model = Badge
        model_fields = ("id", "expiration", "is_active")


@router.get("", response=list[BadgeSchema])
def badges(request):
    badges = Badge.objects.all()
    return badges


@router.get("{sid}", response=BadgeSchema)
def badge(request, sid: str):
    return get_object_or_404(Badge, sid=sid)

from ninja import ModelSchema, Router

from .models.badge import Badge

router = Router()


class BadgeSchema(ModelSchema):
    class Config:
        model = Badge
        model_fields = ("id", "expiration", "is_active")


@router.get("", response=list[BadgeSchema])
def badges(request):
    badges = Badge.objects.all()
    return badges

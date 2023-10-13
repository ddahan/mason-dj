from django.shortcuts import get_object_or_404

from ninja import Router

from .models.badge import Badge
from .schemas import BadgeSchemaInCreate, BadgeSchemaInUpdate, BadgeSchemaOut

router = Router()


@router.get("", response=list[BadgeSchemaOut])
def list_badges(request):
    return Badge.objects.all()


@router.get("{sid}", response=BadgeSchemaOut)
def retrieve_badge(request, sid: str):
    return get_object_or_404(Badge, sid=sid)


@router.post("", response=BadgeSchemaOut)
def create_badge(request, payload: BadgeSchemaInCreate):
    return Badge.objects.create(owner=request.auth, **payload.dict())


@router.put("{sid}", response=BadgeSchemaOut)
def update_badge(request, sid: str, payload: BadgeSchemaInUpdate):
    badge = get_object_or_404(Badge, sid=sid)
    for field, value in payload.dict().items():
        setattr(badge, field, value)
    badge.save()
    return badge


@router.patch("{sid}", response=BadgeSchemaOut)
def update_badge_activity(request, sid: str):
    """Example of a more specific update that deals with a single field"""

    badge = get_object_or_404(Badge, sid=sid)
    badge.invert_activity()
    return badge


@router.delete("{sid}")
def destroy_badge(request, sid: str):
    badge = get_object_or_404(Badge, sid=sid)
    badge.delete()

from django.shortcuts import get_object_or_404

from ninja import Router
from ninja.pagination import PageNumberPagination, paginate

from .models.badge import Badge
from .schemas import BadgeSchemaInCreate, BadgeSchemaInUpdate, BadgeSchemaOut

router = Router()

# There is no authentication here to help trying not mixing and coupling concepts together, as there is already a specifing app dealing with quathentication.


@router.get("", response=list[BadgeSchemaOut], auth=None)
@paginate(PageNumberPagination, page_size=10)
def list_badges(request):
    return Badge.objects.all()


@router.get("{identifier}", response=BadgeSchemaOut, auth=None)
def retrieve_badge(request, identifier: str):
    return get_object_or_404(Badge, identifier=identifier)


@router.post("", response=BadgeSchemaOut)
def create_badge(request, payload: BadgeSchemaInCreate):
    return Badge.objects.create(owner=request.auth, **payload.dict())


@router.put("{identifier}", response=BadgeSchemaOut)
def update_badge(request, identifier: str, payload: BadgeSchemaInUpdate):
    """This accept partial updates by excluding unset fields."""

    badge = get_object_or_404(Badge, identifier=identifier)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(badge, field, value)
    badge.save()
    return badge


# TODO: here: add update_badge_partiel but let the user choose the field


@router.patch("{identifier}/activity", response=BadgeSchemaOut)
def update_badge_activity(request, identifier: str):
    """Example of a more RPC-Like endpoint which perform a specific mutation, without
    providing a payload"""

    badge = get_object_or_404(Badge, identifier=identifier)
    badge.invert_activity()
    return badge


@router.delete("{identifier}")
def destroy_badge(request, identifier: str):
    badge = get_object_or_404(Badge, identifier=identifier)
    badge.delete()

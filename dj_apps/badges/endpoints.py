from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from ninja import Router
from ninja.pagination import paginate

from api.ordering import Ordering, ordering
from api.pagination import MyPageNumberPagination
from api.searching import Searching, searching

from .models.badge import Badge
from .schemas import BadgeSchemaIn, BadgeSchemaOut

router = Router()

User = get_user_model()

# There is no authentication here to help trying not mixing and coupling concepts together, as there is already a specifing app dealing with quathentication.


@router.get("", response=list[BadgeSchemaOut], auth=None)
@paginate(MyPageNumberPagination)
@ordering(Ordering)
@searching(Searching, search_fields=["owner__first_name", "owner__last_name"])
def list_badges(request):
    return Badge.objects.all()


@router.get("{identifier}", response=BadgeSchemaOut, auth=None)
def retrieve_badge(request, identifier: str):
    return get_object_or_404(Badge, identifier=identifier)


@router.post("", response=BadgeSchemaOut, auth=None)
def create_badge(request, payload: BadgeSchemaIn):
    return Badge.objects.create(**payload.dict())


@router.put("{identifier}", response=BadgeSchemaOut, auth=None)
def update_badge(request, identifier: str, payload: BadgeSchemaIn):
    """Update a badge entirely"""

    badge = get_object_or_404(Badge, identifier=identifier)
    for field, value in payload.dict().items():
        setattr(badge, field, value)
    badge.save()
    return badge


@router.patch("{identifier}", response=BadgeSchemaOut, auth=None)
def update_badge_partial(request, identifier: str, payload: BadgeSchemaIn):
    """Update a badge by patching provided fields only"""
    # NOTE: untested/unused - could require to update BadgeSchemaIn accordingly

    badge = get_object_or_404(Badge, identifier=identifier)
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(badge, field, value)
    badge.save()
    return badge


@router.patch("{identifier}/activity", response=BadgeSchemaOut, auth=None)
def update_badge_activity(request, identifier: str):
    """Example of a more RPC-Like endpoint which perform a specific mutation, without
    providing a payload"""

    badge = get_object_or_404(Badge, identifier=identifier)
    badge.invert_activity()
    return badge


@router.delete("{identifier}", auth=None)
def destroy_badge(request, identifier: str):
    badge = get_object_or_404(Badge, identifier=identifier)
    badge.delete()

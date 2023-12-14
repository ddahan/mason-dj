from django.contrib.auth import get_user_model

from ninja import Router
from ninja.pagination import paginate

from api.pagination import MyPageNumberPagination
from api.searching import Searching, searching

from .schemas import OwnerBadgeSchemaOut

User = get_user_model()

router = Router()


@router.get("", response=list[OwnerBadgeSchemaOut], auth=None)
@paginate(MyPageNumberPagination)
@searching(Searching, search_fields=["first_name", "last_name"])
def list_users(request):
    return User.objects.all()

from typing import Any

from ninja import Field, Schema
from ninja.pagination import PaginationBase


class MyPageNumberPagination(PaginationBase):
    """This is inspirated by
    https://github.com/vitalik/django-ninja/issues/993#issuecomment-1848605438"""

    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: int = Field(10, ge=1, le=50)

    class Output(Schema):
        nb_items: int = Field(ge=1)
        item_start: int = Field(ge=1)
        item_end: int = Field(ge=1)
        nb_pages: int = Field(ge=1)
        page_size: int = Field(ge=1)
        page: int = Field(ge=1)

    def paginate_queryset(self, queryset, pagination: Input, request, **kwargs) -> Any:
        offset = (pagination.page - 1) * pagination.page_size
        nb_items = self._items_count(queryset)

        return {
            "nb_items": nb_items,
            "item_start": offset + 1,
            "item_end": min(offset + pagination.page_size, nb_items),
            "nb_pages": (nb_items + pagination.page_size - 1) // pagination.page_size,
            "page_size": pagination.page_size,
            "page": pagination.page,
            "items": queryset[offset : offset + pagination.page_size],
        }

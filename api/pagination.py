from typing import Any

from django.core.exceptions import FieldError

from ninja import Field, Schema
from ninja.pagination import PaginationBase

from core.exceptions import APIFieldException


class MyPageNumberPagination(PaginationBase):
    class Input(Schema):
        page: int = Field(1, ge=1)
        order_by: str = None  # contains both the sorting field AND the direction

    class Output(Schema):
        nb_items: int = Field(ge=1)
        item_start: int = Field(ge=1)
        item_end: int = Field(ge=1)
        nb_pages: int = Field(ge=1)
        page_size: int = Field(ge=1)
        page: int = Field(ge=1)

    def __init__(self, page_size=10, **kwargs):
        self.page_size = page_size
        super().__init__(**kwargs)

    def paginate_queryset(self, queryset, pagination: Input, request) -> Any:
        if pagination.order_by:
            try:
                queryset = queryset.order_by(pagination.order_by)
            except FieldError:
                raise APIFieldException(wrong_field=pagination.order_by)

        offset = (pagination.page - 1) * self.page_size
        nb_items = self._items_count(queryset)

        return {
            "nb_items": nb_items,
            "item_start": offset + 1,
            "item_end": min(offset + self.page_size, nb_items),
            "nb_pages": (nb_items + self.page_size - 1) // self.page_size,
            "page_size": self.page_size,
            "page": pagination.page,
            "items": queryset[offset : offset + self.page_size],
        }

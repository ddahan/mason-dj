from typing import Any

from ninja import Field, Schema
from ninja.pagination import PaginationBase


class MyPageNumberPagination(PaginationBase):
    class Input(Schema):
        page: int = Field(1, ge=1)

    class Output(Schema):
        nb_items: int
        nb_pages: int
        page: int
        previous_page: str | None
        next_page: str | None

    def __init__(self, page_size: int = 100, **kwargs):
        self.page_size = page_size
        super().__init__(**kwargs)

    def paginate_queryset(self, queryset, pagination: Input, request) -> Any:
        offset = (pagination.page - 1) * self.page_size
        nb_items = self._items_count(queryset)
        next_page, previous_page = None, None
        if pagination.page > 1:
            previous_page = request.build_absolute_uri(
                request.path + "?page=" + str(pagination.page - 1)
            )
        if offset + self.page_size < nb_items:
            next_page = request.build_absolute_uri(
                request.path + "?page=" + str(pagination.page + 1)
            )
        return {
            "nb_items": nb_items,
            "nb_pages": (nb_items + self.page_size - 1) // self.page_size,
            "page": pagination.page,
            "previous_page": previous_page,
            "next_page": next_page,
            "items": queryset[offset : offset + self.page_size],
        }

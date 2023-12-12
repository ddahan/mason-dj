"""
inspired by https://eadwincode.github.io/django-ninja-extra/tutorial/ordering/
(typing updated to 3.12 + async removed)
"""

import inspect
from abc import ABC, abstractmethod
from functools import wraps
from operator import attrgetter, itemgetter
from typing import (
    Any,
    Callable,
    Type,
    overload,
)

from django.db.models import QuerySet

from ninja import Field, Query, Schema
from ninja.constants import NOT_SET
from pydantic import BaseModel

from .extras import add_ninja_contribute_args

__all__ = [
    "OrderingBase",
    "Ordering",
    "ordering",
    "OrderatorOperation",
]


class OrderingBase(ABC):
    class Input(Schema):
        ...

    InputSource = Query(...)

    def __init__(self, *, pass_parameter: str | None = None, **kwargs: Any) -> None:
        self.pass_parameter = pass_parameter

    @abstractmethod
    def ordering_queryset(
        self, items: QuerySet | list, ordering_input: Any
    ) -> QuerySet | list:
        ...


class Ordering(OrderingBase):
    class Input(Schema):
        ordering: str | None = Field(None)

    def __init__(
        self,
        ordering_fields: list[str] | None = None,
        pass_parameter: str | None = None,
    ) -> None:
        super().__init__(pass_parameter=pass_parameter)
        self.ordering_fields = ordering_fields or "__all__"

    def ordering_queryset(
        self, items: QuerySet | list, ordering_input: Input
    ) -> QuerySet | list:
        ordering = self.get_ordering(items, ordering_input.ordering)
        if ordering:
            if isinstance(items, QuerySet):  # type:ignore
                return items.order_by(*ordering)
            elif isinstance(items, list) and items:

                def multisort(xs: list, specs: list[tuple[str, bool]]) -> list:
                    orerator = itemgetter if isinstance(xs[0], dict) else attrgetter
                    for key, reverse in specs:
                        xs.sort(key=orerator(key), reverse=reverse)
                    return xs

                return multisort(
                    items,
                    [(o[int(o.startswith("-")) :], o.startswith("-")) for o in ordering],
                )
        return items

    def get_ordering(self, items: QuerySet | list, value: str | None) -> list[str]:
        if value:
            fields = [param.strip() for param in value.split(",")]
            return self.remove_invalid_fields(items, fields)
        return []

    def remove_invalid_fields(
        self, items: QuerySet | list, fields: list[str]
    ) -> list[str]:
        valid_fields = list(self.get_valid_fields(items))

        def term_valid(term: str) -> bool:
            if term.startswith("-"):
                term = term[1:]
            return term in valid_fields

        return [term for term in fields if term_valid(term)]

    def get_valid_fields(self, items: QuerySet | list) -> list[str]:
        valid_fields: list[str] = []
        if self.ordering_fields == "__all__":
            if isinstance(items, QuerySet):  # type:ignore
                valid_fields = self.get_all_valid_fields_from_queryset(items)
            elif isinstance(items, list):
                valid_fields = self.get_all_valid_fields_from_list(items)
        else:
            valid_fields = list(self.ordering_fields)
        return valid_fields

    def get_all_valid_fields_from_queryset(self, items: QuerySet) -> list[str]:
        return [str(field.name) for field in items.model._meta.fields] + [
            str(key) for key in items.query.annotations
        ]

    def get_all_valid_fields_from_list(self, items: list) -> list[str]:
        if not items:
            return []
        item = items[0]
        if isinstance(item, BaseModel):
            return list(item.model_fields.keys())
        if isinstance(item, dict):
            return list(item.keys())
        if hasattr(item, "_meta") and hasattr(item._meta, "fields"):
            return [str(field.name) for field in item._meta.fields]
        return []


@overload
def ordering() -> Callable[..., Any]:  # pragma: no cover
    ...


@overload
def ordering(
    func_or_ordering_class: Any = NOT_SET, **paginator_params: Any
) -> Callable[..., Any]:  # pragma: no cover
    ...


def ordering(
    func_or_ordering_class: Any = NOT_SET, **ordering_params: Any
) -> Callable[..., Any]:
    isfunction = inspect.isfunction(func_or_ordering_class)
    isnotset = func_or_ordering_class == NOT_SET

    ordering_class: Type[OrderingBase] = "Ordering"

    if isfunction:
        return _inject_orderator(func_or_ordering_class, ordering_class)

    if not isnotset:
        ordering_class = func_or_ordering_class

    def wrapper(func: Callable[..., Any]) -> Any:
        return _inject_orderator(func, ordering_class, **ordering_params)

    return wrapper


def _inject_orderator(
    func: Callable[..., Any],
    ordering_class: Type[OrderingBase],
    **ordering_params: Any,
) -> Callable[..., Any]:
    orderator: OrderingBase = ordering_class(**ordering_params)
    orderator_kwargs_name = "ordering"
    orderator_operation_class = OrderatorOperation
    orderator_operation = orderator_operation_class(
        orderator=orderator, view_func=func, orderator_kwargs_name=orderator_kwargs_name
    )

    return orderator_operation.as_view


class OrderatorOperation:
    def __init__(
        self,
        *,
        orderator: OrderingBase,
        view_func: Callable,
        orderator_kwargs_name: str = "ordering",
    ) -> None:
        self.orderator = orderator
        self.orderator_kwargs_name = orderator_kwargs_name
        self.view_func = view_func

        orderator_view = self.get_view_function()
        _ninja_contribute_args: list[tuple] = getattr(
            self.view_func, "_ninja_contribute_args", []
        )
        orderator_view._ninja_contribute_args = (  # type:ignore[attr-defined]
            _ninja_contribute_args
        )
        add_ninja_contribute_args(
            orderator_view,
            (
                self.orderator_kwargs_name,
                self.orderator.Input,
                self.orderator.InputSource,
            ),
        )
        orderator_view.orderator_operation = self  # type:ignore[attr-defined]
        self.as_view = wraps(view_func)(orderator_view)

    @property
    def view_func_has_kwargs(self) -> bool:  # pragma: no cover
        return self.orderator.pass_parameter is not None

    def get_view_function(self) -> Callable:
        def as_view(controller: Any, *args: Any, **kw: Any) -> Any:
            func_kwargs = dict(**kw)
            ordering_params = func_kwargs.pop(self.orderator_kwargs_name)
            if self.orderator.pass_parameter:
                func_kwargs[self.orderator.pass_parameter] = ordering_params

            items = self.view_func(controller, *args, **func_kwargs)
            return self.orderator.ordering_queryset(items, ordering_params)

        return as_view

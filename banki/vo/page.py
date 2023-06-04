from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, PositiveInt
from pydantic.generics import GenericModel

_EntityType = TypeVar('_EntityType')


class Page(BaseModel):
    cursor: PositiveInt = 1
    size: PositiveInt = 20


class ItemsPage(GenericModel, Generic[_EntityType]):
    items: list[_EntityType]  # noqa: WPS110
    next_cursor: Optional[int]

from typing import Optional
from dataclasses import dataclass, field, fields, asdict


class FieldInfoMixin:
    @classmethod
    def field_names(cls):
        return tuple(field.name for field in fields(cls))

    def as_dict(self):
        return asdict(self)


@dataclass(init=True, repr=True, eq=True, order=True, frozen=True)
class Category(FieldInfoMixin):
    """
    Класс для категорий.
    """

    category_name: str
    subcategory_name: str
    url: str = field(compare=False, hash=False)


@dataclass(init=True, repr=True, eq=True, order=True, frozen=True)
class Product(FieldInfoMixin):
    """
    Класс для продуктов.
    """

    id: str
    description: str = field(compare=False, hash=False)
    number_of_orders: Optional[str] = field(compare=False, hash=False)
    price: Optional[str] = field(compare=False, hash=False)


@dataclass(init=True, repr=True, eq=True, order=True, frozen=True)
class Url(FieldInfoMixin):
    """
    Класс для URL продутов.
    """

    url: str

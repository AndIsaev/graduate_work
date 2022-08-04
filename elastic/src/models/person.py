from typing import Optional

from models.mixin import BaseModelMixin, PaginationMixin
from pydantic import BaseModel


class ElasticPerson(BaseModel):
    id: str
    full_name: str
    roles: Optional[list[str]] = []
    film_ids: Optional[list[dict[str, str]]] = []


class FilmPerson(BaseModelMixin):
    """Schema for Film work detail"""

    full_name: str


class DetailResponsePerson(FilmPerson):
    """Schema for Person detail"""

    role: list[str]
    film_ids: Optional[list[dict[str, str]]] = []


class PersonPagination(PaginationMixin):
    persons: list[DetailResponsePerson] = []

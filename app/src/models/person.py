from typing import Optional
from uuid import UUID

from models.mixin import BaseModelMixin, PaginationMixin
from pydantic import BaseModel


class ElasticPerson(BaseModel):
    id: str
    full_name: str
    roles: Optional[list[str]] = []
    film_ids: Optional[list[UUID]] = []


class FilmPerson(BaseModelMixin):
    """Schema for Film work detail"""

    full_name: str


class DetailResponsePerson(FilmPerson):
    """Schema for Person detail"""

    role: str
    film_ids: Optional[list[UUID]] = []


class PersonPagination(PaginationMixin):
    persons: list[DetailResponsePerson] = []

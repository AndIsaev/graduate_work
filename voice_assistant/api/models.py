from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Person(BaseModel):
    uuid: UUID
    full_name: str


class Genre(BaseModel):
    uuid: UUID
    name: str


class BaseFilm(BaseModel):
    """Фильм в списке."""

    uuid: UUID
    title: str
    rating: float


class Film(BaseFilm):
    """Подробная информация о фильме."""

    description: str
    genre: Optional[list[Genre]]
    actors: Optional[list[Person]]
    writers: Optional[list[Genre]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    directors_names: Optional[list[str]]

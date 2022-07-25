from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Person(BaseModel):
    uuid: UUID
    full_name: str


class Genre(BaseModel):
    uuid: UUID
    name: str


class FilmBase(BaseModel):
    """Фильм в списке."""

    uuid: UUID
    title: str
    imdb_rating: float


class Film(FilmBase, BaseModel):
    """Подробная информация о фильме."""

    description: str
    genre: Optional[List[Genre]]
    actors: Optional[List[Person]]
    writers: Optional[List[Genre]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]
    directors_names: Optional[List[str]]

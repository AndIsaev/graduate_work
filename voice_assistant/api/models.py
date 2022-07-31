from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Person(BaseModel):
    uuid: UUID
    full_name: str


class Genre(BaseModel):
    uuid: UUID
    name: str


class FilmGenre(BaseModel):
    id: str
    name: str


class BaseFilm(BaseModel):
    """Фильм в списке."""

    uuid: UUID
    title: str
    imdb_rating: float
    description: str
    genre: Optional[list[FilmGenre]]


class Film(BaseFilm):
    """Подробная информация о фильме."""

    actors: Optional[list[Person]]
    writers: Optional[list[Person]]
    directors: Optional[list[Person]]

from typing import Optional

from .genre_schema import FilmGenreValidation
from .mixin import PaginationValidation, UUIDValidation
from .person_schema import FilmPersonValidation


class ListFilmValidation(UUIDValidation):

    title: str
    imdb_rating: Optional[float] = None


class DetailResponseFilm(ListFilmValidation):
    """Schema for Film work detail"""

    description: Optional[str] = None
    genre: Optional[list[FilmGenreValidation]] = []
    actors: Optional[list[FilmPersonValidation]] = []
    writers: Optional[list[FilmPersonValidation]] = []
    directors: Optional[list[FilmPersonValidation]] = []


class FilmPaginationValidation(PaginationValidation):
    films: list[ListFilmValidation] = []

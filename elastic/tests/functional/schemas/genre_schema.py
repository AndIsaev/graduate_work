from .mixin import PaginationValidation, UUIDValidation


class FilmGenreValidation(UUIDValidation):

    name: str


class GenrePaginationValidation(PaginationValidation):
    genres: list[FilmGenreValidation] = []

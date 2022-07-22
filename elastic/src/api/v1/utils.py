from typing import Optional

from fastapi import Query


class FilmQueryParams:
    """
    Класс задает параметры для поиска по фильму
    """

    def __init__(
        self,
        sort_imdb_rating: Optional[str] = Query(
            None,
            title="Сортировка по рейтингу",
            description="Сортирует по возрастанию и убыванию,"
            " -field если нужна сортировка по убыванию или field,"
            " если нужна сортировка по возрастанию",
            alias="sort",
        ),
        genre_filter: Optional[str] = Query(
            None,
            title="Фильтр жанров",
            description="Фильтрует фильмы по жанрам",
            alias="filter[genre]",
        ),
        query: Optional[str] = Query(
            None,
            title="Запрос",
            description="Осуществляет поиск по названию фильма",
        ),
    ) -> None:
        self.sort = (sort_imdb_rating,)
        self.genre_filter = genre_filter
        self.query = query


class PersonSearchParam:
    """
    Класс задает параметры для поиска персоны по имени
    """

    def __init__(
        self,
        query: str = Query(
            default="John",
            example="Jake",
            title="Запрос",
            description="Осуществляет поиск по имени персоны",
        ),
    ) -> None:
        self.query = query

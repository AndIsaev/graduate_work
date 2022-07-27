"""Implements connector to Movie Async API for search info about movies, people, genres."""

from http import HTTPStatus
from typing import Dict, List, Optional, Tuple
from uuid import UUID

import requests

from .models import Film, BaseFilm, Person


class SearchConnector:
    def __init__(self, url: str) -> None:
        self._url = url

    def _get_response(self, path: str, query: Optional[Dict] = None) -> requests.Response:
        response = requests.get(f"{self._url}{path}", params=query)
        return response

    def find_film_data(self, search_str: str) -> Optional[Film]:
        film_uuid = self._find_film_uuid(search_str)
        film = self._get_film_by_uuid(film_uuid)
        return film

    def find_film_directors(self, search_str: str) -> Tuple[Optional[str], Optional[str]]:
        film = self.find_film_data(search_str)
        if not film:
            return None, None
        return film.title, ", ".join(film.directors_names)

    def find_film_actors(self, search_str: str, limit: int = 5) -> Tuple[Optional[str], Optional[str]]:
        film = self.find_film_data(search_str)
        if not film:
            return None, None
        return film.title, ", ".join(film.actors_names[:limit])

    def find_top_films(self, genre_id: Optional[UUID], page: int = 1) -> Optional[List[BaseFilm]]:
        films = self._find_films(genre_id=genre_id, page=page)
        return films

    def find_person_films(self, search_str: str) -> Tuple[Optional[str], Optional[str]]:
        person = self._find_person(search_str)
        if not person:
            return None, None
        films = self._get_films_by_person_uuid(person.uuid)
        film_names = ", ".join(film.title for film in films) if films else None
        return person.full_name, film_names

    def _find_film_uuid(self, search_str: str) -> Optional[UUID]:
        response = self._get_response(
            "film/search",
            query={
                "query_string": search_str,
                "page[size]": 1,
                "page[number]": 1,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None
        return response.json()[0]["uuid"]

    def _get_film_by_uuid(self, film_uuid: UUID) -> Optional[Film]:
        response = self._get_response(f"film/{film_uuid}")
        if response.status_code != HTTPStatus.OK:
            return None
        return Film(**response.json())

    def _find_films(self, genre_id: Optional[UUID], page: int = 1, size: int = 3) -> Optional[List[BaseFilm]]:
        response = self._get_response(
            "film/",
            query={
                "filter[genre]": genre_id,
                "page[size]": size,
                "page[number]": page,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None
        return [BaseFilm(**row) for row in response.json()]

    def _find_person(self, search_str: str) -> Optional[Person]:
        response = self._get_response(
            "person/",
            query={
                "search[name]": search_str,
                "page[size]": 1,
                "page[number]": 1,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None
        return Person(**response.json()[0])

    def _get_films_by_person_uuid(self, person_uuid: UUID) -> Optional[List[Film]]:
        response = self._get_response(f"person/{person_uuid}")
        if response.status_code != HTTPStatus.OK:
            return None
        film_ids = response.json()["film_ids"][:5]
        films = []
        for film_id in film_ids:
            film = self._get_film_by_uuid(film_id)
            if film:
                films.append(film)
        return films

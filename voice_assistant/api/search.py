"""Implements connector to Movie Async API for search info about movies, people, genres."""

from http import HTTPStatus
from typing import Optional
from uuid import UUID

import requests

from .models import Film, BaseFilm, Person


class SearchConnector:
    def __init__(self, url: str) -> None:
        self._url = url

    def _get_response(self, path: str, query: Optional[dict] = None) -> requests.Response:
        response = requests.get(f"{self._url}{path}", params=query)
        return response

    def find_film_by_name(self, film_name: str) -> Optional[list[BaseFilm]]:
        films = self._find_films(film_name=film_name, page=1, size=1)
        if films:
            return self._find_film_by_uuid(films[0].uuid)
        return None

    def find_top_films(self) -> Optional[list[BaseFilm]]:
        films = self._find_films()
        return films

    def find_top_films_by_genre(self, genre_id: Optional[UUID]) -> Optional[list[BaseFilm]]:
        films = self._find_films(genre_id=genre_id)
        return films

    def find_film_actors(
            self, film_uuid: Optional[UUID] = None, film_name: Optional[str] = None, limit: int = 5
    ) -> Optional[list[Person]]:
        return self._find_film_person("actor", film_uuid=film_uuid, film_name=film_name, limit=limit)

    def find_film_directors(
            self, film_uuid: Optional[UUID] = None, film_name: Optional[str] = None, limit: int = 5
    ) -> Optional[list[Person]]:
        return self._find_film_person("director", film_uuid=film_uuid, film_name=film_name, limit=limit)

    def find_person_films(self, search_str: str) -> tuple[Optional[str], Optional[str]]:
        person = self._find_person(search_str)
        if not person:
            return None, None
        films = self._get_films_by_person_uuid(person.uuid)
        film_names = ", ".join(film.title for film in films) if films else None
        return person.full_name, film_names

    def _find_film_by_uuid(self, film_uuid: UUID) -> Optional[Film]:
        response = self._get_response(f"film/{film_uuid}")
        if response.status_code != HTTPStatus.OK:
            return None
        return Film(**response.json())

    def _find_films(
        self, film_name: Optional[str] = None, genre_id: Optional[UUID] = None, page: int = 1, size: int = 3
    ) -> Optional[list[BaseFilm]]:
        query = {
            "sort": "-imdb_rating",
            "page": page,
            "page_size": size,
        }
        if genre_id:
            query["filter[genre]"] = genre_id
        if film_name:
            query["query"] = film_name
        response = self._get_response("film/", query=query)
        if response.status_code != HTTPStatus.OK:
            return None
        response_json = response.json()
        if not response_json.get("total", 0):
            return None
        return [BaseFilm(**row) for row in response_json.get("films", [])]

    def _find_film_person(
        self, person_type: str, film_uuid: Optional[UUID], film_name: Optional[str],  limit: int
    ) -> Optional[list[Person]]:
        film = None
        if film_uuid:
            film = self._find_film_by_uuid(film_uuid)
        elif film_name:
            base_film = self._find_films(film_name=film_name, page=1, size=1)
            if base_film:
                film = self._find_film_by_uuid(base_film[0].uuid)
        if film:
            if person_type == "actor":
                return film.actors[:limit]
            elif person_type == "director":
                return film.directors[:limit]
            elif person_type == "writer":
                return film.writers[:limit]
        return None

    def _find_person(self, search_str: str) -> Optional[Person]:
        response = self._get_response(
            "person/search",
            query={
                "query": search_str,
                "page": 1,
                "page_size": 1,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None
        return Person(**response.json()[0])

    def _get_films_by_person_uuid(self, person_uuid: UUID) -> Optional[list[Film]]:
        response = self._get_response(
            f"person/{person_uuid}/films",
            query={
                "page": 1,
                "page_size": 1,
            },
        )
        if response.status_code != HTTPStatus.OK:
            return None
        film_ids = response.json()["film_ids"][:5]
        films = []
        for film_id in film_ids:
            film = self._find_film_by_uuid(film_id)
            if film:
                films.append(film)
        return films

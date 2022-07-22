import asyncio
from http import HTTPStatus

import pytest

from ..schemas.movie_schema import FilmPaginationValidation
from ..schemas.person_schema import DetailPersonValidation, PersonPaginationValidation
from ..settings import Settings
from ..testdata import film_work_data, person_data
from ..utils.hash_key_creater import create_hash_key

pytestmark = pytest.mark.asyncio


async def test_person_by_id(person_index, make_get_request, redis_cache):
    for person in person_data:
        person_id: str = person.get("id")
        # Выполнение запроса
        response = await make_get_request(endpoint=f"person/{person_id}")
        response_body = response.body
        # Проверка результата Elastic
        assert response.status == HTTPStatus.OK
        assert DetailPersonValidation(**response_body)
        assert response_body.get("uuid") == person_id
        assert response_body.get("full_name") == person.get("full_name")
        assert response_body.get("role") in person.get("roles")
        assert response_body.get("film_ids") == person.get("film_ids")
        # Проверка результата Redis
        assert await redis_cache.get(key=person_id) is not None
        await redis_cache.flushall()
        assert await redis_cache.get(key=person_id) is None


async def test_search_person(person_index, make_get_request, redis_cache):
    test_person: dict = person_data[1]
    query: str = "Jake"
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint="person/search", params={"query": query})
    response_body = response.body
    response_person: dict = response_body.get("persons")[0]
    # Проверка результата Elastic
    assert PersonPaginationValidation(**response_body)
    assert response.status == HTTPStatus.OK
    assert response_person.get("uuid") == test_person.get("id")
    assert response_person.get("full_name") == test_person.get("full_name")
    assert query in test_person.get("full_name")
    assert response_person.get("role") in test_person.get("roles")
    assert response_person.get("film_ids") == test_person.get("film_ids")
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    key: str = create_hash_key(
        index=Settings.PERSON_INDEX, params=f"{total}{page}{page_size}{query}"
    )
    assert await redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None


async def test_person_films(movies_index, person_index, make_get_request, redis_cache):
    test_person: dict = person_data[-1]
    person_id: str = test_person.get("id")
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint=f"person/{person_id}/films/")
    response_body = response.body
    response_films = response_body.get("films")
    film_instances: list[dict] = [
        obj for obj in film_work_data if obj.get("id") in test_person.get("film_ids")
    ]
    # Проверка результата Elastic
    assert response.status == HTTPStatus.OK
    assert FilmPaginationValidation(**response_body)
    assert len(response_films) == len(film_instances)
    for response_film in response_films:
        for film_instance in film_instances:
            if film_instance.get("id") == response_film.get("uuid"):
                assert film_instance.get("id") == response_film.get("uuid")
                assert film_instance.get("title") == response_film.get("title")
                assert film_instance.get("imdb_rating") == response_film.get(
                    "imdb_rating"
                )
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    key: str = create_hash_key(
        index="person_films", params=f"person_films{total}{page}{page_size}{person_id}"
    )
    assert await redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None

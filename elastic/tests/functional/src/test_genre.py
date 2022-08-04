import asyncio
from http import HTTPStatus

import pytest

from elastic.tests.functional.schemas.genre_schema import FilmGenreValidation, GenrePaginationValidation
from elastic.tests.functional.settings import Settings
from elastic.tests.functional.testdata.data_genre import genre_data
from elastic.tests.functional.utils.hash_key_creater import create_hash_key

pytestmark = pytest.mark.asyncio


async def test_list_genre(genre_index, make_get_request, redis_cache):
    await asyncio.sleep(3)
    # Выполнение запроса
    response = await make_get_request(endpoint="genre/")
    response_body = response.body
    response_genres = response_body.get("genres")
    # Проверка результата Elastic
    assert response.status == HTTPStatus.OK
    assert GenrePaginationValidation(**response_body)
    assert response_body.get("total") == len(genre_data)
    for genre in genre_data:
        for response_genre in response_genres:
            if genre.get("id") == response_genre.get("uuid"):
                assert genre.get("id") == response_genre.get("uuid")
                assert genre.get("name") == response_genre.get("name")
    # Проверка результата Redis
    page: int = response_body.get("page")
    page_size: int = response_body.get("page_size")
    total: int = response_body.get("total")
    key: str = create_hash_key(index=Settings.GENRE_INDEX, params=f"{total}{page}{page_size}")
    assert await redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None


async def test_genre_by_id(genre_index, make_get_request, redis_cache):
    for test_genre in genre_data:
        genre_id: str = test_genre.get("id")
        # Выполнение запроса
        response = await make_get_request(endpoint=f"genre/{genre_id}")
        response_body = response.body
        # Проверка результата Elastic
        assert response.status == HTTPStatus.OK
        assert FilmGenreValidation(**response_body)
        assert test_genre.get("id") == response_body.get("uuid")
        assert test_genre.get("name") == response_body.get("name")
        # Проверка результата Redis
        assert await redis_cache.get(key=genre_id) is not None
        await redis_cache.flushall()
        assert await redis_cache.get(key=genre_id) is None

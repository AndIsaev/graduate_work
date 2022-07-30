import asyncio
from http import HTTPStatus
from typing import Optional

import aioredis
import pytest

from ..settings import Settings
from ..testdata.data_film_work import expected_film_data, not_found_film_data
from ..testdata.films_params import film_list_params, film_search_params
from ..utils.hash_key_creater import create_hash_key
from ..utils.status_films import check_films_result


@pytest.mark.parametrize("endpoint, query, expected_status", [*film_search_params, *film_list_params])
@pytest.mark.asyncio
async def test_get_list_films(
    movies_index,
    make_get_request,
    redis_cache: aioredis,
    endpoint: str,
    query: dict,
    expected_status: int,
):
    await asyncio.sleep(3)
    response = await make_get_request(endpoint=f"{endpoint}", params=query)

    check_films_result(
        status=response.status,
        expected_status=expected_status,
        body=response.body,
        expected_query=query.get("query"),
        expected_page=query.get("page"),
        expected_page_size=query.get("page_size"),
    )
    # Проверка результата Redis
    page: int = response.body.get("page")
    page_size: int = response.body.get("page_size")
    total: int = response.body.get("total")
    sort: Optional[str] = query.get("sort")
    genre: Optional[str] = query.get("genre")
    search: Optional[str] = query.get("query")

    key: str = create_hash_key(
        index=Settings.MOVIES_INDEX,
        params=f"{total}{page}{sort}{page_size}{search}{genre}",
    )

    assert redis_cache.get(key=key) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=key) is None


@pytest.mark.asyncio
async def test_get_film(movies_index, make_get_request, redis_cache):

    response = await make_get_request(endpoint=f"film/{expected_film_data.get('uuid')}")
    await asyncio.sleep(3)

    assert HTTPStatus.OK == response.status
    assert expected_film_data.get("uuid") == response.body.get("uuid")
    assert expected_film_data.get("title") == response.body.get("title")
    assert expected_film_data.get("imdb_rating") == response.body.get("imdb_rating")
    assert expected_film_data.get("description") == response.body.get("description")
    assert expected_film_data.get("genre") == response.body.get("genre")
    assert expected_film_data.get("actors") == response.body.get("actors")
    assert expected_film_data.get("writers") == response.body.get("writers")
    assert expected_film_data.get("directors") == response.body.get("directors")

    assert redis_cache.get(key=expected_film_data.get("uuid")) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=expected_film_data.get("uuid")) is None

    # проверка несуществуеего фильма
    response = await make_get_request(endpoint=f"film/{not_found_film_data.get('uuid')}")
    assert HTTPStatus.NOT_FOUND == response.status
    assert redis_cache.get(key=expected_film_data.get("uuid")) is not None
    await redis_cache.flushall()
    assert await redis_cache.get(key=expected_film_data.get("uuid")) is None

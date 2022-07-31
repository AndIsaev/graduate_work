import asyncio
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from ..functional import es_index, testdata
from ..functional.settings import Settings
from ..functional.testdata.data_inserter import es_index_loader


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=Settings.ELASTIC_URL)
    yield client
    await client.close()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture()
async def redis_cache():
    cache = await aioredis.create_redis_pool(
        (Settings.REDIS_HOST, Settings.REDIS_PORT), minsize=10, maxsize=20
    )
    await cache.flushall()
    yield cache
    cache.close()
    await cache.wait_closed()


@pytest.fixture
async def person_index(es_client):
    index: str = Settings.PERSON_INDEX
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.PERSON_INDEX_BODY,
        row_data=testdata.person_data,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
async def genre_index(es_client):
    index: str = Settings.GENRE_INDEX
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.GENRE_INDEX_BODY,
        row_data=testdata.genre_data,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
async def movies_index(es_client):
    index: str = Settings.MOVIES_INDEX
    await es_index_loader(
        es_client=es_client,
        index=index,
        index_body=es_index.FILM_WORK_INDEX_BODY,
        row_data=testdata.film_work_data,
    )
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture
def make_get_request(session):
    async def inner(endpoint: str = None, params: dict = None) -> HTTPResponse:
        """
        :param endpoint: str
            Путь до нашего конечного url
        :param params: Optional[dict]
            Параметры для запроса
        :return:
        """
        params = params or {}
        url = f"{Settings.SERVICE_URL}/api/v1/{endpoint}"
        async with session.get(url=url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner

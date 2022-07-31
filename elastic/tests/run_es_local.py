import asyncio

from elasticsearch import AsyncElasticsearch
from elasticsearch._async.helpers import async_bulk
from functional import es_index, testdata
from functional.settings import Settings


async def es_index_loader(index: str, index_body: dict, row_data: list[dict]) -> None:
    client = AsyncElasticsearch(hosts="localhost:9200")
    await client.indices.create(index=index, body=index_body, ignore=400)
    await insert_data_in_es(client=client, index=index, row_data=row_data)
    await client.close()


async def data_gather(row_data: list[dict], index: str) -> list[dict]:

    return [{"_index": index, "_id": obj.get("id"), **obj} for obj in row_data]


async def insert_data_in_es(client, index: str, row_data: list[dict]) -> None:
    data = await data_gather(row_data=row_data, index=index)
    await async_bulk(client=client, actions=data)


async def movies_index() -> None:
    index: str = Settings.MOVIES_INDEX
    row_data = testdata.film_work_data

    await es_index_loader(index=index, index_body=es_index.FILM_WORK_INDEX_BODY, row_data=row_data)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(movies_index())
    loop.close()

from elasticsearch._async.helpers import async_bulk


async def es_index_loader(es_client, index: str, index_body: dict, row_data: list[dict]):
    # Создание индекса в Elastic
    await es_client.indices.create(index=index, body=index_body, ignore=400)
    # Заполнение данных для теста
    await insert_data_in_es(client=es_client, index=index, row_data=row_data)


async def data_gather(row_data: list[dict], index: str) -> list[dict]:
    return [{"_index": index, "_id": obj.get("id"), **obj} for obj in row_data]


async def insert_data_in_es(client, index: str, row_data: list[dict]):
    data = await data_gather(row_data=row_data, index=index)
    await async_bulk(client=client, actions=data)

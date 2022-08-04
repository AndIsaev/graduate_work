from typing import Any, Optional, Union

from core.config import CACHE_EXPIRE_IN_SECONDS
from db.cache import AbstractCache
from db.storage import AbstractStorage
from elasticsearch import NotFoundError


class ServiceMixin:
    def __init__(self, cache: AbstractCache, storage: AbstractStorage, index: str) -> None:
        self.cache: AbstractCache = cache
        self.storage: AbstractStorage = storage
        self.index: str = index
        self.total_count: int = 0

    async def get_total_count(self) -> int:
        return self.total_count

    async def set_total_count(self, value: int):
        self.total_count = value

    async def search_in_elastic(self, body: dict, _source=None, sort=None, _index=None) -> Any:
        if not _index:
            _index = self.index

        sort_field = sort[0] if not isinstance(sort, str) and sort else sort
        if sort_field:
            order = "desc" if sort_field.startswith("-") else "asc"
            sort_field = f"{sort_field.removeprefix('-')}:{order}"
        try:
            return await self.storage.search(
                index=_index,
                _source=_source,
                body=body,
                sort=sort_field,
            )
        except Exception:
            return None

    async def get_by_id(self, target_id: str, schema):
        """Пытаемся получить данные из кеша, потому что оно работает быстрее"""
        instance = await self._get_result_from_cache(key=target_id)
        if not instance:
            """Если данных нет в кеше, то ищем его в Elasticsearch"""
            instance = await self._get_data_from_elastic_by_id(target_id=target_id, schema=schema)
            if not instance:
                return None
            """ Сохраняем фильм в кеш """
            await self._put_data_to_cache(key=instance.id, instance=instance.json())  # type: ignore
            return instance
        return schema.parse_raw(instance)

    async def _get_data_from_elastic_by_id(self, target_id: str, schema):
        """Если он отсутствует в Elastic, значит объекта вообще нет в базе"""
        try:
            doc = await self.storage.get(index=self.index, target_id=target_id)
            return schema(**doc["_source"])
        except NotFoundError:
            return None

    async def _get_result_from_cache(self, key: str) -> Optional[bytes]:
        """Пытаемся получить данные об объекте из кеша"""
        return await self.cache.get(key=key) or None  # type: ignore

    async def _put_data_to_cache(self, key: str, instance: Union[bytes, str]) -> None:
        """Сохраняем данные об объекте в кеш, время жизни кеша — 5 минут"""
        await self.cache.set(key=key, value=instance, expire=CACHE_EXPIRE_IN_SECONDS)

from typing import Optional, Union

from db.cache import AbstractCache


class CacheRedis(AbstractCache):
    async def get(self, key: str) -> Optional[dict]:
        return await self.cache.get(key=key)

    async def set(self, key: str, value: Union[bytes, str], expire: int):
        await self.cache.set(key=key, value=value, expire=expire)

    async def close(self) -> None:
        await self.cache.close()

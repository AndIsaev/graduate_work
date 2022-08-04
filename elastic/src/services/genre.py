from functools import lru_cache
from typing import Optional

import orjson
from core.config import GENRE_INDEX
from db.cache import AbstractCache, get_cache
from db.storage import AbstractStorage, get_storage
from fastapi import Depends
from models.genre import ElasticGenre, FilmGenre
from services.mixins import ServiceMixin
from services.pagination import get_by_pagination
from services.utils import create_hash_key, get_hits


class GenreService(ServiceMixin):

    # get_genres_list возвращает список объектов жанра
    async def get_genres_list(self, page: int, page_size: int) -> Optional[dict]:
        body: dict = {
            "size": page_size,
            "from": (page - 1) * page_size,
            "query": {"match_all": {}},
        }
        """ Получаем число фильмов из стейт """
        state_total: int = await self.get_total_count()
        params: str = f"{state_total}{page}{page_size}"
        """ Пытаемся получить данные из кэша """
        instance = await self._get_result_from_cache(
            key=create_hash_key(index=self.index, params=params)
        )
        if not instance:
            docs: Optional[dict] = await self.search_in_elastic(body=body)
            if not docs:
                return None
            """ Получаем жанры из ES """
            hits = get_hits(docs=docs, schema=ElasticGenre)
            """ Получаем число жанров """
            total: int = int(docs.get("hits").get("total").get("value", 0))
            """ Прогоняем данные через pydantic """
            genres: list[FilmGenre] = [
                FilmGenre(uuid=es_genre.id, name=es_genre.name) for es_genre in hits
            ]
            """ Сохраняем жанры в кеш """
            data = orjson.dumps([i.dict() for i in genres])
            new_param: str = f"{total}{page}{page_size}"
            await self._put_data_to_cache(
                key=create_hash_key(index=self.index, params=new_param), instance=data
            )
            """ Сохраняем число жанров в стейт """
            await self.set_total_count(value=total)
            return get_by_pagination(
                name="genres",
                db_objects=genres,
                total=total,
                page=page,
                page_size=page_size,
            )

        return get_by_pagination(
            name="genres",
            db_objects=[FilmGenre(**row) for row in orjson.loads(instance)],
            total=state_total,
            page=page,
            page_size=page_size,
        )


# get_genre_service — это провайдер GenreService. Синглтон
@lru_cache()
def get_genre_service(
    cache: AbstractCache = Depends(get_cache),
    storage: AbstractStorage = Depends(get_storage),
) -> GenreService:
    return GenreService(cache=cache, storage=storage, index=GENRE_INDEX)

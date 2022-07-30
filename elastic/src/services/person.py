from functools import lru_cache
from http import HTTPStatus
from typing import Optional

import orjson
from core.config import PERSON_INDEX
from db.cache import AbstractCache, get_cache
from db.storage import AbstractStorage, get_storage
from fastapi import Depends, HTTPException
from models.person import DetailResponsePerson, ElasticPerson
from services.mixins import ServiceMixin
from services.pagination import get_by_pagination
from services.utils import create_hash_key, get_hits


class PersonService(ServiceMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.person_films: int = 0

    async def get_person_films_count(self) -> int:
        return self.person_films

    async def set_person_films_count(self, value: int):
        self.person_films = value

    async def get_person(self, person_id: str):
        person = await self.get_by_id(target_id=person_id, schema=ElasticPerson)
        if not person:
            """Если персона не найдена, отдаём 404 статус"""
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="person not found"
            )
        return person

    async def search_person(
        self, query: Optional[str], page: int, page_size: int
    ) -> Optional[dict]:
        if not query:
            body = {
                "size": page_size,
                "from": (page - 1) * page_size,
                "query": {
                    "bool": {
                        "must": {
                            "match_all": {},
                        }
                    }
                },
            }
        else:
            body = {
                "size": page_size,
                "from": (page - 1) * page_size,
                "query": {
                    "bool": {
                        "must": {
                            "match": {
                                "full_name": {"query": query, "fuzziness": "auto"}
                            }
                        },
                    }
                },
            }
        """ Получаем число персон из стейт """
        state_total: int = await self.get_total_count()
        params: str = f"{state_total}{page}{page_size}{query}"
        """ Пытаемся получить данные из кэша """
        instance = await self._get_result_from_cache(
            key=create_hash_key(index=self.index, params=params)
        )
        if not instance:
            docs: Optional[dict] = await self.search_in_elastic(
                body=body, _index="persons"
            )
            if not docs:
                return None
            """ Получаем персон из ES """
            hits = get_hits(docs=docs, schema=ElasticPerson)
            """ Получаем число персон """
            total: int = int(docs.get("hits").get("total").get("value", 0))
            """ Прогоняем данные через pydantic """
            persons: list[DetailResponsePerson] = [
                DetailResponsePerson(
                    uuid=es_person.id,
                    full_name=es_person.full_name,
                    role=es_person.roles,
                    film_ids=es_person.film_ids,
                )
                for es_person in hits
            ]
            """ Сохраняем персон в кеш """
            data = orjson.dumps([i.dict() for i in persons])
            new_param: str = f"{total}{page}{page_size}{query}"
            await self._put_data_to_cache(
                key=create_hash_key(index=self.index, params=new_param), instance=data
            )
            """ Сохраняем число персон в стейт """
            await self.set_total_count(value=total)
            return get_by_pagination(
                name="persons",
                db_objects=persons,
                total=total,
                page=page,
                page_size=page_size,
            )

        return get_by_pagination(
            name="persons",
            db_objects=[DetailResponsePerson(**row) for row in orjson.loads(instance)],
            total=state_total,
            page=page,
            page_size=page_size,
        )


# get_person_service — это провайдер PersonService. Синглтон
@lru_cache()
def get_person_service(
    cache: AbstractCache = Depends(get_cache),
    storage: AbstractStorage = Depends(get_storage),
) -> PersonService:
    return PersonService(cache=cache, storage=storage, index=PERSON_INDEX)

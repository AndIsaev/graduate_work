from functools import lru_cache
from http import HTTPStatus
from typing import Optional

import orjson
from db.cache import AbstractCache, get_cache
from db.storage import AbstractStorage, get_storage
from fastapi import Depends, HTTPException
from models.film import ESFilm, ListResponseFilm
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

    async def get_person_films(
        self, film_ids: list[str], page: int, page_size: int, person_id: str
    ) -> Optional[dict]:
        """Получаем число фильмов персоны из стейт"""
        state_total: int = await self.get_person_films_count()
        body: dict = {
            "size": page_size,
            "from": (page - 1) * page_size,
            "query": {"ids": {"values": film_ids}},
        }
        state_key: str = "person_films"
        params: str = f"{state_total}{page}{page_size}{person_id}"
        """ Пытаемся получить фильмы персоны из кэша """
        instance = await self._get_result_from_cache(
            key=create_hash_key(index=self.index, params=params)
        )
        if not instance:
            docs: Optional[dict] = await self.search_in_elastic(
                body=body, _index="movies_test"
            )
            if not docs:
                return None
            """ Получаем фильмы персоны из ES """
            hits = get_hits(docs=docs, schema=ESFilm)
            """ Получаем число фильмов персоны """
            total: int = int(docs.get("hits").get("total").get("value", 0))
            """ Прогоняем данные через pydantic """
            person_films: list[ListResponseFilm] = [
                ListResponseFilm(
                    uuid=film.id, title=film.title, imdb_rating=film.imdb_rating
                )
                for film in hits
            ]
            data = orjson.dumps([i.dict() for i in person_films])
            new_param: str = f"person_films{total}{page}{page_size}{person_id}"
            await self._put_data_to_cache(
                key=create_hash_key(index=state_key, params=new_param), instance=data
            )
            """ Сохраняем число персон в стейт """
            await self.set_person_films_count(value=total)
            return get_by_pagination(
                name="films",
                db_objects=person_films,
                total=total,
                page=page,
                page_size=page_size,
            )
        person_films: list[ListResponseFilm] = [
            ListResponseFilm(**row) for row in orjson.loads(instance)
        ]
        return get_by_pagination(
            name="films",
            db_objects=person_films,
            total=state_total,
            page=page,
            page_size=page_size,
        )

    async def search_person(
        self, query: str, page: int, page_size: int
    ) -> Optional[dict]:
        body: dict = {
            "size": page_size,
            "from": (page - 1) * page_size,
            "query": {"bool": {"must": [{"match": {"full_name": query}}]}},
        }
        """ Получаем число персон из стейт """
        state_total: int = await self.get_total_count()
        params: str = f"{state_total}{page}{page_size}{query}"
        """ Пытаемся получить данные из кэша """
        instance = await self._get_result_from_cache(
            key=create_hash_key(index=self.index, params=params)
        )
        if not instance:
            docs: Optional[dict] = await self.search_in_elastic(body=body)
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
                    role=es_person.roles[0],
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
        persons: list[DetailResponsePerson] = [
            DetailResponsePerson(**row) for row in orjson.loads(instance)
        ]
        return get_by_pagination(
            name="persons",
            db_objects=persons,
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
    return PersonService(cache=cache, storage=storage, index="person_test")

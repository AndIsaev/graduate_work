import hashlib
from typing import Optional

from pydantic import parse_obj_as
from services.mixins import Schemas


def get_params_films_to_elastic(
    page_size: int = 10, page: int = 1, genre: str = None, query: str = None
) -> dict:
    """
    :param page:
    :param page_size:
    :param genre: фильтрует фильмы по жанру
    :param query: находит фильмы по полю title
    :return: возвращает правильный body для поиска в Elasticsearch
    """
    films_search = None
    if genre:
        films_search = {"fuzzy": {"genre": {"value": genre}}}
    if query:
        body: dict = {
            "size": page_size,
            "from": (page - 1) * page_size,
            "query": {
                "bool": {
                    "must": {"match": {"title": {"query": query, "fuzziness": "auto"}}},
                    "filter": films_search,
                }
            },
        }
    else:
        body: dict = {
            "size": page_size,
            "from": (page - 1) * page_size,
            "query": {
                "bool": {
                    "must": {
                        "match_all": {},
                    },
                    "filter": films_search,
                }
            },
        }
    return body


def get_hits(docs: Optional[dict], schema: Schemas):
    hits: dict = docs.get("hits").get("hits")
    data: list = [row.get("_source") for row in hits]
    return parse_obj_as(list[schema], data)


def create_hash_key(index: str, params: str) -> str:
    """
    :param index: индекс в elasticsearch
    :param params: параметры запроса
    :return: хешированый ключ в md5
    """
    hash_key = hashlib.md5(params.encode()).hexdigest()
    return f"{index}:{hash_key}"

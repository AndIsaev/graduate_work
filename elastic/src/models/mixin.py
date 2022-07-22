from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes,
    # а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseModelMixin(BaseModel):
    uuid: UUID

    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class PaginationMixin(BaseModel):
    """
    Definition of Pagination Schema

    Attributes
    ----------
    total: int
        size of achievement list
    page: int
        selected page number
    page_size: int
        page size
    next_page: Optional[int], default = None
        next page of achievements
    previous_page: Optional[int], default = None
        previous page of achievements
    available_pages: int
        available pages
    """

    total: int
    page: int
    page_size: int
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    available_pages: int

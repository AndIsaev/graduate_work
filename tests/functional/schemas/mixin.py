from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UUIDValidation(BaseModel):
    uuid: UUID


class PaginationValidation(BaseModel):
    total: int
    page: int
    page_size: int
    next_page: Optional[int] = None
    previous_page: Optional[int] = None
    available_pages: int

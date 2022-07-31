from http import HTTPStatus
from typing import Optional

from api.v1.utils import PersonSearchParam
from fastapi import APIRouter, Depends, HTTPException
from models.person import DetailResponsePerson, PersonPagination
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(
    path="/",
    response_model=PersonPagination,
    summary="Поиск персоны по его имени",
    description="Поиск персоны по его имени",
    response_description="Список персон с их именем, ролью и фильмографией",
    tags=["person_service"],
)
async def person_search(
    params: PersonSearchParam = Depends(),
    person_service: PersonService = Depends(get_person_service),
    page: int = 1,
    page_size: int = 10,
) -> PersonPagination:
    persons: Optional[dict] = await person_service.search_person(
        query=params.query, page=page, page_size=page_size
    )
    if not persons:
        """Если персоны не найдены, отдаём 404 статус"""
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="persons not found"
        )
    return PersonPagination(**persons)


@router.get(
    path="/{person_id}",
    response_model=DetailResponsePerson,
    summary="Поиск персоны по ID",
    description="Поиск персоны по ID",
    response_description="Имя, роль и фильмография персоны",
    tags=["person_service"],
)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> DetailResponsePerson:
    person = await person_service.get_person(person_id=person_id)
    return DetailResponsePerson(
        uuid=person.id,
        full_name=person.full_name,
        role=person.roles,
        film_ids=person.film_ids,
    )

from http import HTTPStatus
from typing import Optional

from api.v1.utils import FilmQueryParams
from fastapi import APIRouter, Depends, HTTPException
from models.film import DetailResponseFilm, ESFilm, FilmPagination
from models.person import FilmPerson
from services.film import FilmService, get_film_service

router = APIRouter()


@router.get(
    path="/",
    response_model=FilmPagination,
    summary="Поиск кинопроизведений",
    description="Полнотекстовый поиск по кинопроизведениям",
    response_description="Название и рейтинг фильма",
    tags=["film_service"],
)
async def search_film_list(
    params: FilmQueryParams = Depends(),
    film_service: FilmService = Depends(get_film_service),
    page: int = 1,
    page_size: int = 10,
) -> FilmPagination:
    films: Optional[dict] = await film_service.get_all_films(
        sorting=params.sort,  # type: ignore
        page=page,
        page_size=page_size,
        query=params.query,
        genre=params.genre_filter,
    )
    if not films:
        """Если фильмы не найдены, отдаём 404 статус"""
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")
    return FilmPagination(**films)


@router.get(
    path="/{film_id}",
    response_model=DetailResponseFilm,
    summary="Поиск кинопроизведения по ID",
    description="Поиск кинопроизведения по ID",
    response_description="Полная информация о фильме",
    tags=["film_service"],
)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> DetailResponseFilm:
    film = await film_service.get_by_id(target_id=film_id, schema=ESFilm)
    if not film:
        """Если фильм не найден, отдаём 404 статус"""
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    actors_list: list[FilmPerson] = [
        FilmPerson(uuid=actor.get("id"), full_name=actor.get("full_name"))
        for actor in film.actors
    ]
    writers_list: list[FilmPerson] = [
        FilmPerson(uuid=writer.get("id"), full_name=writer.get("full_name"))
        for writer in film.writers
    ]
    directors_list: list[FilmPerson] = [
        FilmPerson(uuid=director.get("id"), full_name=director.get("full_name"))
        for director in film.directors
    ]
    return DetailResponseFilm(
        uuid=film.id,
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        actors=actors_list,
        writers=writers_list,
        directors=directors_list,
    )

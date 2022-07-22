from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from models.genre import DetailResponseGenre, ElasticGenre, GenrePagination
from services.genre import GenreService, get_genre_service

router = APIRouter()


@router.get(
    path="/",
    response_model=GenrePagination,
    summary="Список жанров кино",
    description="Список жанров кино",
    response_description="Название жанра",
    tags=["genre_service"],
)
async def genres_list(
    genre_service: GenreService = Depends(get_genre_service),
    page: int = 1,
    page_size: int = 10,
) -> GenrePagination:
    genres: Optional[dict] = await genre_service.get_genres_list(
        page=page, page_size=page_size
    )
    if not genres:
        """Если жанры не найдены, отдаём 404 статус"""
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return GenrePagination(**genres)


@router.get(
    path="/{genre_id}",
    response_model=DetailResponseGenre,
    summary="Поиск жанра по ID",
    description="Поиск жанра по ID",
    response_description="Название жанра",
    tags=["genre_service"],
)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> DetailResponseGenre:
    genre = await genre_service.get_by_id(target_id=genre_id, schema=ElasticGenre)
    if not genre:
        """Если жанр не найден, отдаём 404 статус"""
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return DetailResponseGenre(uuid=genre.id, name=genre.name)

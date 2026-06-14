from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_super_user
from app.core.security import JWTBearer
from app.schema.user import User
from app.schema.genre import FindGenreResult, UpsertGenre, Genre, FindGenreQuery 
from app.service.genre import GenreService


router = APIRouter(
    prefix="/genre", 
    tags=["genre"], 
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=FindGenreResult)
@inject
async def get_genre_list(
    find_query: FindGenreQuery = Depends(),
    service: GenreService = Depends(Provide[Container.genre_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_list(find_query)


@router.post("", response_model=Genre)
@inject
async def create_genre(
    genre: UpsertGenre,
    service: GenreService = Depends(Provide[Container.genre_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.add(genre)


@router.patch("/{genre_id}", response_model=Genre)
@inject
async def update_genre(
    genre_id: int,
    genre: UpsertGenre,
    service: GenreService = Depends(Provide[Container.genre_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.patch(genre_id, genre)



@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_genre(
    genre_id: int,
    service: GenreService = Depends(Provide[Container.genre_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove_by_id(genre_id)
    return None  # При 204 коде FastAPI сам очистит тело ответа

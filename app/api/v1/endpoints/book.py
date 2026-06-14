from typing import List, Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, UploadFile, File as FastAPIFile, status

from app.core.container import Container
from app.core.dependencies import get_current_editor_user, get_current_super_user
from app.schema.book import UpsertBook
from app.schema.user import User
from app.service.book import BookService

router = APIRouter(prefix="/book", tags=["book"])


@router.get("")
@inject
async def get_book_list(
    page: int = 1,
    page_size: int = 10,
    genre_id: Optional[int] = None,
    service: BookService = Depends(Provide[Container.book_service]),
):
    return service.get_list_of_books(page=page, page_size=page_size, genre_id=genre_id)


@router.get("/{book_id}")
@inject
async def get_book(
    book_id: int,
    service: BookService = Depends(Provide[Container.book_service]),
):
    return service.get_detail(book_id)


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
async def create_book(
    title: str = Form(...),
    description: str = Form(""),
    year: int = Form(...),
    publisher: str = Form(...),
    author: str = Form(...),
    volume: int = Form(...),
    genre_ids: str = Form(default=""),    
    cover: UploadFile = FastAPIFile(...),
    service: BookService = Depends(Provide[Container.book_service]),
    current_user: User = Depends(get_current_super_user),
):
    schema = UpsertBook(
        title=title, description=description, year=year,
        publisher=publisher, author=author, volume=volume,
    )
    cover_bytes = await cover.read()
    parsed_genre_ids = [int(g.strip()) for g in genre_ids.split(",") if g.strip()]
    return service.create(schema, parsed_genre_ids, cover_bytes, cover.filename, cover.content_type)


from fastapi import Body

@router.patch("/{book_id}")
@inject
async def update_book(
    book_id: int,
    book: UpsertBook = Body(...),
    genre_ids: Optional[List[int]] = Body(default=None),
    service: BookService = Depends(Provide[Container.book_service]),
    current_user: User = Depends(get_current_editor_user),
):
    return service.update(book_id, book, genre_ids)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_book(
    book_id: int,
    service: BookService = Depends(Provide[Container.book_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove(book_id)
    return None
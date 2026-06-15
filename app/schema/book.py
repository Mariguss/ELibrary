from typing import List, Optional
from pydantic import BaseModel
from app.schema.base import SearchOptions
from app.schema.genre import Genre


class BookBase(BaseModel):
    title: str
    description: str | None = None
    year: int
    publisher: str
    author: str
    volume: int | None = None

    model_config = {"from_attributes": True}


class Book(BookBase):
    id: int


class UpsertBook(BaseModel):
    title: str | None = None
    description: str | None = None
    year: int | None = None
    publisher: str | None = None
    author: str | None = None
    volume: int | None = None

    model_config = {"from_attributes": True}


class BookListItem(Book):
    genres: List[Genre] = []
    avg_rating: float | None = None
    comments_count: int = 0
    cover_url: str | None = None


class FindBookResult(BaseModel):
    founds: List[BookListItem]
    search_options: SearchOptions


class BookDetail(BookListItem):
    pass
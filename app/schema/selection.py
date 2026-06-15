from typing import List
from pydantic import BaseModel
from app.schema.book import BookListItem


class UpsertSelection(BaseModel):
    name: str


class Selection(BaseModel):
    id: int
    name: str
    user_id: int

    model_config = {"from_attributes": True}


class SelectionWithCount(Selection):
    book_count: int = 0


class SelectionDetail(Selection):
    books: List[BookListItem] = []


class AddBookToSelection(BaseModel):
    book_id: int

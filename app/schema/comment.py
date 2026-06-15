from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.schema.base import SearchOptions
from app.schema.user import User


class CommentBase(BaseModel):
    scale: int = Field(ge=0, le=5)
    text: str

    model_config = {"from_attributes": True}


class UpsertComment(BaseModel):
    scale: int = Field(ge=0, le=5)
    text: str


class Comment(CommentBase):
    id: int
    book_id: int
    user_id: int
    created_at: datetime
    user: User


class FindCommentResult(BaseModel):
    founds: List[Comment]
    search_options: SearchOptions

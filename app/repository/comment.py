from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session, joinedload

from app.model.comment import Comment
from app.repository.base import BaseRepository

from sqlalchemy.orm import joinedload
from app.model.user import User
from sqlalchemy import select

class CommentRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Comment)

    def read_by_book(self, book_id: int):
        with self.session_factory() as session:
            query = (
                select(Comment)
                .where(Comment.book_id == book_id)
                .options(
                    joinedload(Comment.user).joinedload(User.role)
                )
                .order_by(Comment.created_at.desc())
            )
            return session.execute(query).unique().scalars().all()

    def find_by_book_and_user(self, book_id: int, user_id: int):
        with self.session_factory() as session:
            return (
                session.query(Comment)
                .options(joinedload(Comment.user))
                .filter(Comment.book_id == book_id, Comment.user_id == user_id)
                .first()
            )
    
    def read_by_id_with_user(self, comment_id: int):
        with self.session_factory() as session:
            query = (
                select(Comment)
                .where(Comment.id == comment_id)
                .options(joinedload(Comment.user).joinedload(User.role))
            )
            return session.execute(query).unique().scalar_one()


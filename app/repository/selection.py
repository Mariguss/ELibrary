from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import DuplicatedError, NotFoundError
from app.model.book import Book
from app.model.bookgenre import BookGenre
from app.model.bookselection import BookSelection
from app.model.selection import Selection
from app.repository.base import BaseRepository


class SelectionRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Selection)

    def read_by_user(self, user_id: int):
        with self.session_factory() as session:
            results = (
                session.query(Selection, func.count(BookSelection.id))
                .outerjoin(BookSelection, BookSelection.selection_id == Selection.id)
                .filter(Selection.user_id == user_id)
                .group_by(Selection.id)
                .all()
            )
            return [
                {"id": s.id, "name": s.name, "user_id": s.user_id, "book_count": count}
                for s, count in results
            ]

    def read_detail(self, selection_id: int, user_id: int):
        with self.session_factory() as session:
            selection = (
                session.query(Selection)
                .filter(Selection.id == selection_id, Selection.user_id == user_id)
                .first()
            )
            if not selection:
                raise NotFoundError(detail=f"not found id : {selection_id}")

            books = (
                session.query(Book)
                .join(BookSelection, BookSelection.book_id == Book.id)
                .options(joinedload(Book.book_genres).joinedload(BookGenre.genre))
                .filter(BookSelection.selection_id == selection_id)
                .all()
            )

            from app.repository.book import BookRepository
            book_repo = BookRepository(self.session_factory)
            return {
                "id": selection.id,
                "name": selection.name,
                "user_id": selection.user_id,
                "books": [book_repo._enrich(session, book) for book in books],
            }

    def add_book(self, selection_id: int, user_id: int, book_id: int):
        with self.session_factory() as session:
            selection = (
                session.query(Selection)
                .filter(Selection.id == selection_id, Selection.user_id == user_id)
                .first()
            )
            if not selection:
                raise NotFoundError(detail=f"not found id : {selection_id}")

            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise NotFoundError(detail=f"not found book id : {book_id}")

            existing = (
                session.query(BookSelection)
                .filter(BookSelection.selection_id == selection_id, BookSelection.book_id == book_id)
                .first()
            )
            if existing:
                raise DuplicatedError(detail="Книга уже добавлена в эту подборку")

            try:
                session.add(BookSelection(selection_id=selection_id, book_id=book_id))
                session.commit()
            except Exception:
                session.rollback()
                raise

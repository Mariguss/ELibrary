from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import NotFoundError
from app.model.book import Book
from app.model.bookgenre import BookGenre
from app.model.comment import Comment
from app.model.file import File
from app.repository.base import BaseRepository

import os
from app.core.config import configs

UPLOAD_DIR = os.path.join(configs.PROJECT_ROOT, "uploads", "covers")

class BookRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Book)

    def _enrich(self, session: Session, book: Book) -> dict:
        avg_rating = (
            session.query(func.avg(Comment.scale))
            .filter(Comment.book_id == book.id)
            .scalar()
        )
        comments_count = (
            session.query(func.count(Comment.id))
            .filter(Comment.book_id == book.id)
            .scalar()
        )
        cover = session.query(File).filter(File.book_id == book.id).first()

        cover_url = None
        if cover and os.path.exists(UPLOAD_DIR):
            for fname in os.listdir(UPLOAD_DIR):
                if fname.startswith(f"{cover.id}."):
                    cover_url = f"/uploads/covers/{fname}"
                    break

        return {
            "id": book.id,
            "title": book.title,
            "description": book.description,
            "year": book.year,
            "publisher": book.publisher,
            "author": book.author,
            "volume": book.volume,
            "genres": [bg.genre for bg in book.book_genres],
            "avg_rating": round(avg_rating, 2) if avg_rating is not None else None,
            "comments_count": comments_count or 0,
            "cover_url": cover_url,
        }

    def read_list_with_details(self, page: int = 1, page_size: int = 10, genre_id: int | None = None):
        with self.session_factory() as session:
            query = session.query(Book).options(
                joinedload(Book.book_genres).joinedload(BookGenre.genre)
            )

            if genre_id is not None:
                query = query.join(BookGenre, BookGenre.book_id == Book.id).filter(
                    BookGenre.genre_id == genre_id
                )

            query = query.order_by(Book.year.desc(), Book.id.desc())

            total_count = query.distinct().count()
            books = query.distinct().limit(page_size).offset((page - 1) * page_size).all()

            return {
                "founds": [self._enrich(session, book) for book in books],
                "search_options": {
                    "page": page,
                    "page_size": page_size,
                    "ordering": "-year",
                    "total_count": total_count,
                },
            }

    def read_detail(self, book_id: int):
        with self.session_factory() as session:
            book = (
                session.query(Book)
                .options(joinedload(Book.book_genres).joinedload(BookGenre.genre))
                .filter(Book.id == book_id)
                .first()
            )
            if not book:
                raise NotFoundError(detail=f"not found id : {book_id}")
            return self._enrich(session, book)
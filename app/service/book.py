import hashlib
import os

from app.core.config import configs
from app.core.exceptions import NotFoundError
from app.model.book import Book
from app.model.bookgenre import BookGenre
from app.model.file import File
from app.repository.book import BookRepository
from app.schema.book import UpsertBook
from app.service.base import BaseService
from app.util.sanitize import sanitize_html

UPLOAD_DIR = os.path.join(configs.PROJECT_ROOT, "uploads", "covers")


class BookService(BaseService):
    def __init__(self, repository: BookRepository):
        self.repository = repository
        super().__init__(repository)

    def get_list_of_books(self, page: int = 1, page_size: int = 10, genre_id: int | None = None):
        return self.repository.read_list_with_details(page=page, page_size=page_size, genre_id=genre_id)

    def get_detail(self, book_id: int):
        return self.repository.read_detail(book_id)

    def create(
        self,
        schema: UpsertBook,
        genre_ids: list[int],
        cover_bytes: bytes,
        cover_filename: str | None,
        cover_mime: str | None,
    ):
        if schema.description:
            schema.description = sanitize_html(schema.description)

        session_factory = self.repository.session_factory
        with session_factory() as session:
            try:
                book = Book(**schema.model_dump(exclude_none=True))
                session.add(book)
                session.flush()  # получаем book.id без commit (аналог lastrowid)

                for genre_id in genre_ids:
                    session.add(BookGenre(book_id=book.id, genre_id=genre_id))

                md5_hash = hashlib.md5(cover_bytes).hexdigest()
                existing = session.query(File).filter(File.md5_hash == md5_hash).first()
                if existing:
                    cover_file = existing
                else:
                    cover_file = File(
                        name=cover_filename or "cover",
                        mime_type=cover_mime or "application/octet-stream",
                        md5_hash=md5_hash,
                        book_id=book.id,
                    )
                    session.add(cover_file)
                    session.flush()

                session.commit()
            except Exception:
                session.rollback()
                raise

            book_id = book.id
            cover_file_id = cover_file.id
            cover_is_new = existing is None

        # Файл на диск пишем только после успешного commit в БД
        if cover_is_new:
            ext = os.path.splitext(cover_filename or "")[1]
            os.makedirs(UPLOAD_DIR, exist_ok=True)
            with open(os.path.join(UPLOAD_DIR, f"{cover_file_id}{ext}"), "wb") as f:
                f.write(cover_bytes)

        return self.repository.read_detail(book_id)

    def update(self, book_id: int, schema: UpsertBook, genre_ids: list[int] | None):
        if schema.description:
            schema.description = sanitize_html(schema.description)

        session_factory = self.repository.session_factory
        with session_factory() as session:
            try:
                book = session.query(Book).filter(Book.id == book_id).first()
                if not book:
                    raise NotFoundError(detail=f"not found id : {book_id}")

                for key, value in schema.model_dump(exclude_none=True).items():
                    setattr(book, key, value)

                if genre_ids is not None:
                    session.query(BookGenre).filter(BookGenre.book_id == book_id).delete()
                    for genre_id in genre_ids:
                        session.add(BookGenre(book_id=book_id, genre_id=genre_id))

                session.commit()
            except Exception:
                session.rollback()
                raise

        return self.repository.read_detail(book_id)

    def remove(self, book_id: int):
        session_factory = self.repository.session_factory
        with session_factory() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise NotFoundError(detail=f"not found id : {book_id}")

            cover = session.query(File).filter(File.book_id == book_id).first()
            cover_id = cover.id if cover else None

            try:
                session.delete(book)
                session.commit()
            except Exception:
                session.rollback()
                raise

        if cover_id and os.path.exists(UPLOAD_DIR):
            for fname in os.listdir(UPLOAD_DIR):
                if fname.startswith(f"{cover_id}."):
                    os.remove(os.path.join(UPLOAD_DIR, fname))
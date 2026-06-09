from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import Base

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.book import Book
    from app.model.genre import Genre
    
class BookGenre(Base):
    __tablename__ = "book_genre"

    book_id: Mapped[int] = mapped_column(nullable=False)
    genre_id: Mapped[int] = mapped_column(nullable=False)

    book = relationship("Book", back_populates="genres")
    genre = relationship("Genre", back_populates="books")

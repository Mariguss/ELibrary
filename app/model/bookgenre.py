from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import BaseModel
from sqlalchemy import ForeignKey, UniqueConstraint
from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.book import Book
    from app.model.genre import Genre
    
class BookGenre(BaseModel):
    __tablename__ = "book_genre"
    __table_args__ = (
        # Ensure that a book can only be associated with a genre once        
        UniqueConstraint("book_id", "genre_id", name="uix_book_genre"),
    )

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id", ondelete="CASCADE"))

    book = relationship("Book", back_populates="book_genres")
    genre = relationship("Genre", back_populates="book_genres")

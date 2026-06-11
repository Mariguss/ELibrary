from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import BaseModel

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.comment import Comment
    from app.model.file import File
    from app.model.bookselection import BookSelection
    from app.model.bookgenre import BookGenre

class Book(BaseModel):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    volume: Mapped[int] = mapped_column(nullable=True)
    
    comments = relationship("Comment", back_populates="book")
    files = relationship("File", back_populates="book")
    
    book_genres = relationship("BookGenre", back_populates="book")
    book_selections = relationship("BookSelection", back_populates="book")



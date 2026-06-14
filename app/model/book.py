from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from app.model.base import BaseModel
from datetime import datetime
from sqlalchemy import DateTime, func

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.comment import Comment
    from app.model.file import File
    from app.model.bookselection import BookSelection
    from app.model.bookgenre import BookGenre

class Book(BaseModel):
    __tablename__ = "book"
    __table_args__ = (
        UniqueConstraint("title", "author", "year", name="uix_book_title_author_year"),
    )

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    volume: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    comments = relationship("Comment", back_populates="book", passive_deletes=True)
    files = relationship("File", back_populates="book", passive_deletes=True)
    
    book_genres = relationship("BookGenre", back_populates="book", passive_deletes=True)
    book_selections = relationship("BookSelection", back_populates="book", passive_deletes=True)



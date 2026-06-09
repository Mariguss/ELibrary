from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint
from app.model.base import BaseModel

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.book import Book
    from app.model.selection import Selection

class BookSelection(BaseModel):
    __tablename__ = "book_selection"
    __table_args__ = (
        # Ensure that a book can only be added once to a selection
        UniqueConstraint("book_id", "selection_id", name="uix_book_selection"),
    )

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    selection_id: Mapped[int] = mapped_column(ForeignKey("selection.id"), nullable=False)

    book = relationship("Book", back_populates="book_selections")
    selection = relationship("Selection", back_populates="book_selections")

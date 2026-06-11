from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import BaseModel

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.bookgenre import BookGenre

class Genre(BaseModel):
    __tablename__ = "genre"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    book_genres = relationship("BookGenre", back_populates="genre")

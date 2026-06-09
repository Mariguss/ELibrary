from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.model.base import Base
from app.model.book import Book

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.book import Book

class Genre(Base):
    __tablename__ = "genre"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="genre") 

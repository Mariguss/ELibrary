from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import Base

class Book(Base):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    year: Mapped[int] = mapped_column(nullable=False)
    publisher: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    volume: Mapped[int] = mapped_column(nullable=True)

    comments = relationship("Comment", back_populates="book")
    files = relationship("File", back_populates="book")

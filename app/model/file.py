from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.model.base import Base

class File(Base):
    __tablename__ = "file"
    name: Mapped[str] = mapped_column(nullable=False)
    mime_type: Mapped[str] = mapped_column(nullable=False)
    md5_hash: Mapped[str] = mapped_column(nullable=False, unique=True)

    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)

    book = relationship("Book", back_populates="files")

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import Base

class Comment(Base):
    __tablename__ = "comment"

    scale: Mapped[int] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)

    user = relationship("User", back_populates="comments")
    book = relationship("Book", back_populates="comments")

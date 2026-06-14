from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.model.base import BaseModel

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.user import User

class Selection(BaseModel):
    __tablename__ = "selection"

    name: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="selections")
    book_selections = relationship("BookSelection", back_populates="selection")

from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import BaseModel

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.user import User

class Role(BaseModel):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    users = relationship("User", back_populates="role")

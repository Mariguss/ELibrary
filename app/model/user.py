from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import  BaseModel

from typing import TYPE_CHECKING  

if TYPE_CHECKING:
    from app.model.role import Role
    from app.model.selection import Selection
    from app.model.comment import Comment

class User(BaseModel):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)

    comments = relationship("Comment", back_populates="user")
    role = relationship("Role", back_populates="users")
    selections = relationship("Selection", back_populates="user")

    eagers = ["role"]  # Репозиторий автоматически сделает joinedload("role")

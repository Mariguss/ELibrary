from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.model.base import Base

class User(Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)

    role = relationship("Role", back_populates="users")
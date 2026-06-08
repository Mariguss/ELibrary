from sqlalchemy import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.model.base import Base

class Role(Base):
    __tablename__ = "role"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    users = relationship("User", back_populates="role")
from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.model.role import Role
from app.repository.base import BaseRepository


class RoleRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Role)

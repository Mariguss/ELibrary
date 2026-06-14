from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.model.genre import Genre
from app.repository.base import BaseRepository


class GenreRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        super().__init__(session_factory, Genre)

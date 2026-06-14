from app.repository.genre import GenreRepository
from app.service.base import BaseService

class GenreService(BaseService):
    def __init__(self, repository: GenreRepository):
        self.repository = repository
        super().__init__(repository)
from app.repository.role import RoleRepository
from app.service.base import BaseService

class RoleService(BaseService):
    def __init__(self, repository: RoleRepository):
        self.repository = repository
        super().__init__(repository)
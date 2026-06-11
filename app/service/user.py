from app.repository.user import UserRepository
from app.service.base import BaseService
from app.core.security import get_password_hash
from app.schema.user import UpsertUser

class UserService(BaseService):
    def __init__(self, repository: UserRepository):
        self.repository = repository
        super().__init__(repository)

    def add(self, schema: UpsertUser):
        hashed_password = get_password_hash(schema.password_hash) if schema.password_hash else None
        schema.password_hash = hashed_password
        
        return self._repository.create(schema)


    def patch(self, id: int, schema: UpsertUser):
        hashed_password = get_password_hash(schema.password_hash) if schema.password_hash else None
        schema.password_hash = hashed_password

        return self._repository.update(id, schema)

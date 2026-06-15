from app.model.selection import Selection
from app.repository.selection import SelectionRepository
from app.schema.selection import UpsertSelection
from app.service.base import BaseService


class SelectionService(BaseService):
    def __init__(self, repository: SelectionRepository):
        self.repository = repository
        super().__init__(repository)

    def get_my_selections(self, user_id: int):
        return self.repository.read_by_user(user_id)

    def get_detail(self, selection_id: int, user_id: int):
        return self.repository.read_detail(selection_id, user_id)

    def create(self, user_id: int, schema: UpsertSelection):
        session_factory = self.repository.session_factory
        with session_factory() as session:
            try:
                selection = Selection(name=schema.name, user_id=user_id)
                session.add(selection)
                session.commit()
                session.refresh(selection)
            except Exception:
                session.rollback()
                raise
            return {"id": selection.id, "name": selection.name, "user_id": selection.user_id}

    def add_book(self, selection_id: int, user_id: int, book_id: int):
        self.repository.add_book(selection_id, user_id, book_id)

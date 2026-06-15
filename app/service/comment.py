from app.core.exceptions import DuplicatedError, NotFoundError
from app.model.comment import Comment
from app.repository.comment import CommentRepository
from app.schema.comment import UpsertComment
from app.service.base import BaseService
from app.util.sanitize import sanitize_html


class CommentService(BaseService):
    def __init__(self, repository: CommentRepository):
        self.repository = repository
        super().__init__(repository)

    def get_by_book(self, book_id: int):
        return self.repository.read_by_book(book_id)

    def get_my_review(self, book_id: int, user_id: int):
        return self.repository.find_by_book_and_user(book_id, user_id)

    def create(self, book_id: int, user_id: int, schema: UpsertComment):
        existing = self.repository.find_by_book_and_user(book_id, user_id)
        if existing:
            raise DuplicatedError(detail="Вы уже оставили рецензию на эту книгу")

        session_factory = self.repository.session_factory
        with session_factory() as session:
            try:
                comment = Comment(
                    scale=schema.scale,
                    text=sanitize_html(schema.text),
                    book_id=book_id,
                    user_id=user_id,
                )
                session.add(comment)
                session.commit()
                session.refresh(comment)
            except Exception:
                session.rollback()
                raise
            comment_id = comment.id

        return self.repository.read_by_id_with_user(comment_id)

    def update(self, comment_id: int, schema: UpsertComment, current_user):
        comment = self.repository.read_by_id(comment_id)
        if current_user.role.name not in ("admin", "moderator") and comment.user_id != current_user.id:
            raise NotFoundError(detail="not found")

        sanitized = UpsertComment(scale=schema.scale, text=sanitize_html(schema.text))
        self.repository.update(comment_id, sanitized)
        return self.repository.read_by_id_with_user(comment_id)
    
    def remove(self, comment_id: int, current_user):
        comment = self.repository.read_by_id(comment_id)
        if current_user.role.name not in ("admin", "moderator") and comment.user_id != current_user.id:
            raise NotFoundError(detail="not found")
        self.repository.delete_by_id(comment_id)

from dependency_injector import containers, providers

from app.core.database import db_instance
from app.repository.user import UserRepository
from app.repository.role import RoleRepository
from app.repository.book import BookRepository
from app.repository.genre import GenreRepository
from app.repository.comment import CommentRepository
from app.repository.selection import SelectionRepository

from app.service.auth import AuthService
from app.service.user import UserService
from app.service.role import RoleService
from app.service.book import BookService
from app.service.genre import GenreService
from app.service.comment import CommentService
from app.service.selection import SelectionService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.user",
            "app.api.v1.endpoints.role",
            "app.api.v1.endpoints.book",
            "app.api.v1.endpoints.genre",
            "app.api.v1.endpoints.comment",
            "app.api.v1.endpoints.selection",
            "app.core.dependencies",
        ]
    )

    session_factory = providers.Object(db_instance._session_factory)

    # Repositories
    user_repository = providers.Factory(UserRepository, session_factory=session_factory)
    role_repository = providers.Factory(RoleRepository, session_factory=session_factory)
    book_repository = providers.Factory(BookRepository, session_factory=session_factory)
    genre_repository = providers.Factory(GenreRepository, session_factory=session_factory)
    comment_repository = providers.Factory(CommentRepository, session_factory=session_factory)
    selection_repository = providers.Factory(SelectionRepository, session_factory=session_factory)

    # Services
    user_service = providers.Factory(UserService, repository=user_repository)
    auth_service = providers.Factory(AuthService, repository=user_repository)
    role_service = providers.Factory(RoleService, repository=role_repository)
    book_service = providers.Factory(BookService, repository=book_repository)
    genre_service = providers.Factory(GenreService, repository=genre_repository)
    comment_service = providers.Factory(CommentService, repository=comment_repository)
    selection_service = providers.Factory(SelectionService, repository=selection_repository)




from dependency_injector import containers, providers

from app.core.database import db_instance
from app.repository.user import UserRepository
from app.repository.role import RoleRepository

from app.service.auth import AuthService
from app.service.user import UserService
from app.service.role import RoleService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.user",
            "app.api.v1.endpoints.role",
            "app.core.dependencies",
        ]
    )

    session_factory = providers.Object(db_instance._session_factory)

    # Repositories
    user_repository = providers.Factory(UserRepository, session_factory=session_factory)
    role_repository = providers.Factory(RoleRepository, session_factory=session_factory)

    # Services
    user_service = providers.Factory(UserService, repository=user_repository)
    auth_service = providers.Factory(AuthService, repository=user_repository)
    role_service = providers.Factory(RoleService, repository=role_repository)


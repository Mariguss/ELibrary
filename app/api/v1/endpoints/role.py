from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_super_user
from app.core.security import JWTBearer
from app.schema.user import User
from app.schema.role import FindRoleResult, UpsertRole, Role, FindRoleQuery 
from app.service.role import RoleService


router = APIRouter(
    prefix="/role", 
    tags=["role"], 
    dependencies=[Depends(JWTBearer())]
)


@router.get("", response_model=FindRoleResult)
@inject
async def get_role_list(
    find_query: FindRoleQuery = Depends(),
    service: RoleService = Depends(Provide[Container.role_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.get_list(find_query)


@router.post("", response_model=Role)
@inject
async def create_role(
    role: UpsertRole,
    service: RoleService = Depends(Provide[Container.role_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.add(role)


@router.patch("/{role_id}", response_model=Role)
@inject
async def update_role(
    role_id: int,
    role: UpsertRole,
    service: RoleService = Depends(Provide[Container.role_service]),
    current_user: User = Depends(get_current_super_user),
):
    return service.patch(role_id, role)



@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_role(
    role_id: int,
    service: RoleService = Depends(Provide[Container.role_service]),
    current_user: User = Depends(get_current_super_user),
):
    service.remove_by_id(role_id)
    return None  # При 204 коде FastAPI сам очистит тело ответа

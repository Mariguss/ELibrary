from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_user
from app.schema.selection import (
    AddBookToSelection,
    Selection,
    SelectionDetail,
    SelectionWithCount,
    UpsertSelection,
)
from app.schema.user import User
from app.service.selection import SelectionService

router = APIRouter(prefix="/selection", tags=["selection"])


@router.get("", response_model=list[SelectionWithCount])
@inject
async def get_my_selections(
    service: SelectionService = Depends(Provide[Container.selection_service]),
    current_user: User = Depends(get_current_user),
):
    return service.get_my_selections(current_user.id)


@router.get("/{selection_id}", response_model=SelectionDetail)
@inject
async def get_selection_detail(
    selection_id: int,
    service: SelectionService = Depends(Provide[Container.selection_service]),
    current_user: User = Depends(get_current_user),
):
    return service.get_detail(selection_id, current_user.id)


@router.post("", response_model=Selection, status_code=status.HTTP_201_CREATED)
@inject
async def create_selection(
    selection: UpsertSelection,
    service: SelectionService = Depends(Provide[Container.selection_service]),
    current_user: User = Depends(get_current_user),
):
    return service.create(current_user.id, selection)


@router.post("/{selection_id}/book", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def add_book_to_selection(
    selection_id: int,
    payload: AddBookToSelection,
    service: SelectionService = Depends(Provide[Container.selection_service]),
    current_user: User = Depends(get_current_user),
):
    service.add_book(selection_id, current_user.id, payload.book_id)
    return None

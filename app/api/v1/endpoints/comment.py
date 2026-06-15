from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.core.dependencies import get_current_user
from app.schema.comment import Comment, UpsertComment
from app.schema.user import User
from app.service.comment import CommentService

router = APIRouter(tags=["comment"])


@router.get("/book/{book_id}/comment", response_model=list[Comment])
@inject
async def get_book_comments(
    book_id: int,
    service: CommentService = Depends(Provide[Container.comment_service]),
):
    return service.get_by_book(book_id)


@router.get("/book/{book_id}/comment/me", response_model=Comment | None)
@inject
async def get_my_comment(
    book_id: int,
    service: CommentService = Depends(Provide[Container.comment_service]),
    current_user: User = Depends(get_current_user),
):
    return service.get_my_review(book_id, current_user.id)


@router.post("/book/{book_id}/comment", response_model=Comment, status_code=status.HTTP_201_CREATED)
@inject
async def create_comment(
    book_id: int,
    comment: UpsertComment,
    service: CommentService = Depends(Provide[Container.comment_service]),
    current_user: User = Depends(get_current_user),
):
    return service.create(book_id, current_user.id, comment)


@router.patch("/comment/{comment_id}", response_model=Comment)
@inject
async def update_comment(
    comment_id: int,
    comment: UpsertComment,
    service: CommentService = Depends(Provide[Container.comment_service]),
    current_user: User = Depends(get_current_user),
):
    return service.update(comment_id, comment, current_user)


@router.delete("/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_comment(
    comment_id: int,
    service: CommentService = Depends(Provide[Container.comment_service]),
    current_user: User = Depends(get_current_user),
):
    service.remove(comment_id, current_user)
    return None

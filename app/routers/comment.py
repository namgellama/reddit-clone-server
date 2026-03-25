from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database.db import get_db
from app.services import comment as comment_service
from app.schemas.comment import (
    CommentResponse,
    CommentCreateResponse,
    CommentCreate,
    CommentBase,
    CommentUpdate,
)
from app.schemas.vote import VoteRequest, VoteResponse
from app.services import vote as vote_service
from app.utils.security import CurrentUser, OptionalCurrentUser

router = APIRouter()


"""
    @desc Get all comments
    @route GET /api/v1/posts/:post_id/comments
    @access Public

"""


@router.get("/", response_model=list[CommentResponse])
async def get_comments(
    current_user: OptionalCurrentUser,
    post_id: UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user_id = current_user.id if current_user else None

    return await comment_service.get_all(post_id=post_id, user_id=user_id, db=db)


"""
    @desc Get a comment
    @route GET /api/v1/posts/:post_id/comments/:comment_id
    @access Public

"""


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
    post_id: UUID, comment_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]
):
    return await comment_service.get_by_post_id_and_comment_id(
        post_id=post_id, comment_id=comment_id, db=db
    )


"""
    @desc Create a comment
    @route POST /api/v1/posts/:post_id/comments
    @access Private

"""


@router.post(
    "/", response_model=CommentCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_comment(
    post_id: UUID,
    body: CommentBase,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    payload = CommentCreate(
        **body.model_dump(), user_id=current_user.id, post_id=post_id
    )

    return await comment_service.create(payload=payload, db=db)


"""
    @desc Update a comment
    @route PATCH /api/v1/posts/:post_id/comments/:comment_id
    @access Private

"""


@router.patch("/${comment_id}", response_model=CommentCreateResponse)
async def update_comment(
    post_id: UUID,
    comment_id: UUID,
    body: CommentBase,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    payload = CommentUpdate(
        **body.model_dump(), user_id=current_user.id, post_id=post_id, id=comment_id
    )

    return await comment_service.update(payload=payload, db=db)


"""
    @desc Delete a comment
    @route DELETE /api/v1/posts/:post_id/comments/:comment_id
    @access Private

"""


@router.delete("/${comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    post_id: UUID,
    comment_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await comment_service.delete(
        post_id=post_id, comment_id=comment_id, user_id=current_user.id, db=db
    )


"""
    @desc Toggle comment vote
    @route POST /api/v1/posts/:post_id/comments/:comment_id/votes
    @access Private

"""


@router.post("/{comment_id}/votes", response_model=VoteResponse)
async def toggle_comment_vote(
    post_id: UUID,
    comment_id: UUID,
    body: VoteRequest,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await vote_service.toggle_comment_vote(
        post_id=post_id,
        comment_id=comment_id,
        body=body,
        user_id=current_user.id,
        db=db,
    )

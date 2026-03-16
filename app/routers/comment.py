from typing import Annotated
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database.db import get_db
from app.services import comment as comment_service
from app.schemas.comment import (
    CommentResponse,
    CommentCreate,
    CommentBase,
    CommentUpdate,
)
from app.services import upvote as upvote_service
from app.schemas.upvote import UpvoteResponse
from app.utils.security import CurrentUser

router = APIRouter()


"""
    @desc Get all comments
    @route GET /api/v1/posts/:post_id/comments
    @access Public

"""


@router.get("/", response_model=list[CommentResponse])
async def get_comments(post_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    return await comment_service.get_all(post_id=post_id, db=db)


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


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
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


@router.patch("/${comment_id}", response_model=CommentResponse)
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
    @desc Create comment upvote
    @route POST /api/v1/posts/:post_id/comments/:comment_id/upvotes
    @access Private

"""


@router.post("/{comment_id}/upvotes", response_model=UpvoteResponse)
async def toggle_comment_upvote(
    post_id: UUID,
    comment_id: UUID,
    current_user: CurrentUser,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    upvote = await upvote_service.toggle_comment_upvote(
        post_id, comment_id, current_user.id, db=db
    )

    if upvote:
        response.status_code = status.HTTP_201_CREATED

        return {"upvoted": True, "message": "Comment upvoted"}

    response.status_code = status.HTTP_200_OK

    return {"upvoted": False, "message": "Comment upvote removed"}

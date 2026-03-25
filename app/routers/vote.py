from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.vote import VoteResponse, VoteRequest
from app.utils.security import CurrentUser
from app.services import vote as vote_service
from app.database.db import get_db


router = APIRouter()

"""
    @desc Toggle post vote
    @route POST /api/v1/posts/:post_id/votes
    @access Private

"""


@router.post("/{id}/votes", response_model=VoteResponse)
async def toggle_post_vote(
    id: UUID,
    body: VoteRequest,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await vote_service.toggle_post_vote(
        post_id=id, body=body, user_id=current_user.id, db=db
    )


"""
    @desc Toggle comment vote
    @route POST /api/v1/posts/:post_id/comments/:comment_id/votes
    @access Private

"""


@router.post("/comments/{comment_id}/votes", response_model=VoteResponse)
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

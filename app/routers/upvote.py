from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.services.user import get_current_user
from app.schemas.response import APIResponse
from app.schemas.user import UserResponse
from app.schemas.upvote import UpvoteResponse, UpvoteBase, UpvoteCreate
from app.services import upvote as upvote_service

router = APIRouter()

"""
    @desc Create upvote
    @route POST /api/v1/upvotes
    @access Private

"""


@router.post("/", response_model=APIResponse[UpvoteResponse])
async def toggle_upvote(
    body: UpvoteBase,
    response: Response,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    payload = UpvoteCreate(**body.model_dump(), user_id=current_user.id)
    upvote = await upvote_service.toggle(payload=payload, db=db)

    if payload.post_id:
        message = "Post upvoted" if upvote else "Post upvote removed"
    else:
        message = "Comment upvoted" if upvote else "Comment upvote removed"

    if upvote:
        response.status_code = status.HTTP_201_CREATED
        return APIResponse(
            success=True,
            message=message,
            data=UpvoteResponse(upvoted=True),
        )

    response.status_code = status.HTTP_200_OK
    return APIResponse(
        success=True,
        message=message,
        data=UpvoteResponse(upvoted=False),
    )

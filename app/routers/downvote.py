from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.response import APIResponse
from app.schemas.downvote import DownvoteResponse, DownvoteBase, DownvoteCreate
from app.services import downvote as downvote_service
from app.utils.security import CurrentUser

router = APIRouter()

"""
    @desc Create downvote
    @route POST /api/v1/downvotes
    @access Private

"""


@router.post("/", response_model=APIResponse[DownvoteResponse])
async def toggle_downvote(
    body: DownvoteBase,
    response: Response,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    payload = DownvoteCreate(**body.model_dump(), user_id=current_user.id)
    downvote = await downvote_service.toggle(payload=payload, db=db)

    if payload.post_id:
        message = "Post Downvoted" if downvote else "Post downvote removed"
    else:
        message = "Comment Downvoted" if downvote else "Comment downvote removed"

    if downvote:
        response.status_code = status.HTTP_201_CREATED

        return APIResponse(
            success=True, message=message, data=DownvoteResponse(downvoted=True)
        )

    response.status_code = status.HTTP_200_OK

    return APIResponse(
        success=True, message=message, data=DownvoteResponse(downvoted=False)
    )

from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.config.database import get_db
from app.services import comment as comment_service
from app.schemas.response import APIResponse
from app.schemas.comment import CommentResponse, CommentCreate, CommentBase, CommentUpdate
from app.schemas.user import UserResponse
from app.services.user import get_current_user

router = APIRouter()


@router.get("/", response_model=APIResponse[list[CommentResponse]])
async def get_comments(post_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    comments = await comment_service.get_all(post_id=post_id, db=db)

    return APIResponse(success=True, message="Comments fetched successfully", data=comments)


@router.get("/{comment_id}", response_model=APIResponse[CommentResponse])
async def get_comment(post_id: UUID, comment_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    comment = await comment_service.get_by_id(post_id=post_id, comment_id=comment_id, db=db)

    return APIResponse(success=True, message="Comment fetched successfully", data=comment)


@router.post("/", response_model=APIResponse[CommentResponse])
async def create_comment(post_id: UUID, body: CommentBase, current_user: Annotated[UserResponse, Depends(get_current_user)], db: Annotated[AsyncSession, Depends(get_db)],):
    payload = CommentCreate(**body.model_dump(),
                            user_id=current_user.id, post_id=post_id)
    new_comment = await comment_service.create(payload=payload, db=db)

    return APIResponse(success=True, message="Comment fetched successfully", data=new_comment)


@router.patch("/${comment_id}", response_model=APIResponse[CommentResponse])
async def update_comment(post_id: UUID, comment_id: UUID, body: CommentBase, current_user: Annotated[UserResponse, Depends(get_current_user)], db: Annotated[AsyncSession, Depends(get_db)],):
    payload = CommentUpdate(**body.model_dump(),
                            user_id=current_user.id, post_id=post_id, id=comment_id)
    updated_comment = await comment_service.update(payload=payload, db=db)

    return APIResponse(success=True, message="Comment updated successfully", data=updated_comment)

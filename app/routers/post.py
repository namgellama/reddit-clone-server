from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.config.database import get_db
from app.api.v1.post.post_schema import PostResponse, PostCreate, PostBase, PostDetailsResponse
from app.api.v1.user.user_schema import UserResponse
from app.api.v1.post import post_service
from app.api.v1.user.user_service import get_current_user
from app.shared.schemas.response import APIResponse


router = APIRouter()


@router.get("/", response_model=APIResponse[list[PostResponse]])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    posts = await post_service.get_all(db)
    return APIResponse(success=True, message="Posts fetched successfully", data=posts)


@router.get("/{id}", response_model=APIResponse[PostDetailsResponse])
async def get_post(id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await post_service.get_by_id(id=id, db=db)

    return APIResponse(success=True, message="Post fetched successfully", data=PostDetailsResponse.model_validate(post))


@router.post("/", response_model=APIResponse[PostResponse], status_code=status.HTTP_201_CREATED)
async def create_post(body: PostBase, current_user: Annotated[UserResponse, Depends(get_current_user)], db: Annotated[AsyncSession, Depends(get_db)]):
    payload = PostCreate(**body.model_dump(), user_id=current_user.id)
    new_post = await post_service.create(payload=payload, db=db)

    return APIResponse(success=True, message="Post created successfully", data=new_post)


@router.put("/{id}", response_model=APIResponse[PostResponse])
async def update_post(id: UUID, body: PostBase, current_user: Annotated[UserResponse, Depends(get_current_user)], db: Annotated[AsyncSession, Depends(get_db)]):
    payload = PostCreate(**body.model_dump(), user_id=current_user.id)
    updated_post = await post_service.update(id=id, payload=payload, db=db)

    return APIResponse(success=True, message="Post updated successfully", data=updated_post)


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_post(id: UUID,  db: Annotated[AsyncSession, Depends(get_db)]):
    await post_service.delete(id=id, db=db)

    return APIResponse(success=True, message="Post deleted successfully", data=None)

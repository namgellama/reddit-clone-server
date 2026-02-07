from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.post import (
    PostResponse,
    PostCreate,
    PostBase,
    PostResponse,
    PostUpdate,
    PostResponseWithCount,
)
from app.services import post as post_service
from app.schemas.response import APIResponse
from app.utils.security import CurrentUser


router = APIRouter()

"""
    @desc Get all posts
    @route GET /api/v1/posts
    @access Public

"""


@router.get("/", response_model=APIResponse[list[PostResponseWithCount]])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    posts = await post_service.get_all(db)

    return APIResponse(success=True, message="Posts fetched successfully", data=posts)


"""
    @desc Get a post
    @route GET /api/v1/posts/:id
    @access Public

"""


@router.get("/{id}", response_model=APIResponse[PostResponseWithCount])
async def get_post(id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    post = await post_service.get_by_id(id=id, db=db)

    return APIResponse(
        success=True,
        message="Post fetched successfully",
        data=PostResponseWithCount.model_validate(post),
    )


"""
    @desc Create a post
    @route POST /api/v1/posts
    @access Private

"""


@router.post(
    "/", response_model=APIResponse[PostResponse], status_code=status.HTTP_201_CREATED
)
async def create_post(
    body: PostBase,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    payload = PostCreate(**body.model_dump(), user_id=current_user.id)
    new_post = await post_service.create(payload=payload, db=db)

    return APIResponse(success=True, message="Post created successfully", data=new_post)


"""
    @desc Update a post
    @route PUT /api/v1/posts
    @access Private

"""


@router.put("/{id}", response_model=APIResponse[PostResponse])
async def update_post(
    id: UUID,
    body: PostBase,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    payload = PostUpdate(**body.model_dump(), user_id=current_user.id, id=id)
    updated_post = await post_service.update(payload=payload, db=db)

    return APIResponse(
        success=True, message="Post updated successfully", data=updated_post
    )


"""
    @desc Delete a post
    @route DELETE /api/v1/posts/:id
    @access Private

"""


@router.delete("/{id}", response_model=APIResponse[None])
async def delete_post(
    id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await post_service.delete(id=id, user_id=current_user.id, db=db)

    return APIResponse(success=True, message="Post deleted successfully", data=None)

from typing import Annotated, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.schemas.post import (
    PostResponse,
    PostCreate,
    PostCreateResponse,
    PostUpdate,
)
from app.schemas.vote import VoteRequest, VoteResponse
from app.services import post as post_service
from app.services import vote as vote_service
from app.services.image import ImageService
from app.utils.security import CurrentUser, OptionalCurrentUser


router = APIRouter()

"""
    @desc Get all posts
    @route GET /api/v1/posts
    @access Public

"""


@router.get("/", response_model=list[PostResponse])
async def get_posts(
    current_user: OptionalCurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user_id = current_user.id if current_user else None

    return await post_service.get_all(user_id=user_id, db=db)


"""
    @desc Get a post
    @route GET /api/v1/posts/:id
    @access Public

"""


@router.get("/{id}", response_model=PostResponse)
async def get_post(
    id: UUID,
    current_user: OptionalCurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    user_id = current_user.id if current_user else None

    return await post_service.get_by_id(id=id, user_id=user_id, db=db)


"""
    @desc Create a post
    @route POST /api/v1/posts
    @access Private

"""


@router.post(
    "/", response_model=PostCreateResponse, status_code=status.HTTP_201_CREATED
)
async def create_post(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    title: str = Form(...),
    content: str = Form(...),
    images: list[UploadFile] = File(default=[]),
):
    image_list = await ImageService.validate_and_process(images) if images else []

    payload = PostCreate(
        title=title, content=content, images=image_list, user_id=current_user.id
    )

    return await post_service.create(payload=payload, db=db)


"""
    @desc Update a post
    @route PATCH /api/v1/posts
    @access Private

"""


@router.patch("/{id}", response_model=PostCreateResponse)
async def update_post(
    id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    previous_images: list[str] | None = Form(default=None),
    images: list[UploadFile] | None = File(default=None),
):
    image_list = await ImageService.validate_and_process(images) if images else []

    payload = PostUpdate(
        title=title,
        content=content,
        images=image_list,
        previous_images=previous_images,
        user_id=current_user.id,
        id=id,
    )

    return await post_service.update(payload=payload, db=db)


"""
    @desc Delete a post
    @route DELETE /api/v1/posts/:id
    @access Private

"""


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await post_service.delete(id=id, user_id=current_user.id, db=db)


"""
    @desc Toggle post vote
    @route POST /api/v1/posts/:id/votes
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

from typing import Annotated, Optional
from uuid import UUID
from fastapi import APIRouter, Response, Depends, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.schemas.post import (
    PostResponse,
    PostCreate,
    PostUpdate,
    PostResponseWithCount,
)
from app.schemas.upvote import UpvoteResponse
from app.schemas.downvote import DownvoteResponse
from app.services import post as post_service
from app.services import upvote as upvote_service
from app.services import downvote as downvote_service
from app.services.image import ImageService
from app.utils.security import CurrentUser


router = APIRouter()

"""
    @desc Get all posts
    @route GET /api/v1/posts
    @access Public

"""


@router.get("/", response_model=list[PostResponseWithCount])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    return await post_service.get_all(db)


"""
    @desc Get a post
    @route GET /api/v1/posts/:id
    @access Public

"""


@router.get("/{id}", response_model=PostResponseWithCount)
async def get_post(id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    return await post_service.get_by_id(id=id, db=db)


"""
    @desc Create a post
    @route POST /api/v1/posts
    @access Private

"""


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
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


@router.patch("/{id}", response_model=PostResponse)
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
    @desc Toggle post upvote
    @route POST /api/v1/posts/:id/upvotes
    @access Private

"""


@router.post("/{id}/upvotes", response_model=UpvoteResponse)
async def toggle_post_upvote(
    id: UUID,
    current_user: CurrentUser,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    upvote = await upvote_service.toggle_post_upvote(id, current_user.id, db=db)

    if upvote:
        response.status_code = status.HTTP_201_CREATED

        return {"upvoted": True, "message": "Post upvoted"}

    response.status_code = status.HTTP_200_OK

    return {"upvoted": False, "message": "Post upvote removed"}


"""
    @desc Toggle post downvote
    @route POST /api/v1/posts/:id/downvotes
    @access Private

"""


@router.post("/{id}/downvotes", response_model=DownvoteResponse)
async def toggle_post_downvote(
    id: UUID,
    current_user: CurrentUser,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    upvote = await downvote_service.toggle_post_downvote(id, current_user.id, db=db)

    if upvote:
        response.status_code = status.HTTP_201_CREATED

        return {"downvoted": True, "message": "Post downvoted"}

    response.status_code = status.HTTP_200_OK

    return {"downvoted": False, "message": "Post downvote removed"}

from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select, func, distinct
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.models.comment import Comment
from app.models.upvote import Upvote
from app.models.downvote import Downvote
from app.schemas.post import PostCreate, PostUpdate
from app.services.image import ImageService


# Get all
async def get_all(db: AsyncSession):
    stmt = (
        select(
            Post,
            func.count(distinct(Comment.id)).label("comment_count"),
            func.count(distinct(Upvote.id)).label("upvote_count"),
            func.count(distinct(Downvote.id)).label("downvote_count"),
        )
        .outerjoin(Comment, Comment.post_id == Post.id)
        .outerjoin(Upvote, Upvote.post_id == Post.id)
        .outerjoin(Downvote, Downvote.post_id == Post.id)
        .options(selectinload(Post.author))
        .group_by(Post.id)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        {
            **post.__dict__,
            "count": {
                "comment": c_count,
                "upvote": u_count,
                "downvote": d_count,
            },
        }
        for post, c_count, u_count, d_count in rows
    ]


# Fetch by id
async def fetch_by_id(id: UUID, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")

    return post


# Get by id
async def get_by_id(id: UUID, db: AsyncSession):
    stmt = (
        select(
            Post,
            func.count(Comment.id).label("comment_count"),
            func.count(Upvote.id).label("upvote_count"),
            func.count(Downvote.id).label("downvote_count"),
        )
        .outerjoin(Comment, Comment.post_id == Post.id)
        .outerjoin(Upvote, Upvote.post_id == Post.id)
        .outerjoin(Downvote, Downvote.post_id == Post.id)
        .options(selectinload(Post.author))
        .where(Post.id == id)
        .group_by(Post.id)
    )

    result = await db.execute(stmt)
    row = result.first()

    if not row:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found")

    post, c_count, u_count, d_count = row

    return {
        **post.__dict__,
        "count": {
            "comment": c_count,
            "upvote": u_count,
            "downvote": d_count,
        },
    }


# Create
async def create(payload: PostCreate, db: AsyncSession):
    new_post = Post(
        title=payload.title,
        content=payload.content,
        images=payload.images,
        user_id=payload.user_id,
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=["author"])

    return new_post


# Update
async def update(payload: PostUpdate, db: AsyncSession):
    post = await fetch_by_id(id=payload.id, db=db)

    if post.user_id != payload.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    old_images = post.images or []
    previous_images = payload.previous_images or []
    new_images = payload.images or []

    if payload.title is not None:
        post.title = payload.title

    if payload.content is not None:
        post.content = payload.content

    if payload.images is not None or payload.previous_images is not None:
        post.images = previous_images + new_images

    await db.commit()
    await db.refresh(post, attribute_names=["author"])

    if len(previous_images) > 0:
        for image in old_images:
            if image not in previous_images:
                ImageService.delete_image(image)
    else:
        for image in old_images:
            ImageService.delete_image(image)

    return post


# Delete
async def delete(id: UUID, user_id: UUID, db: AsyncSession):
    post = await get_by_id(id=id, db=db)

    if post.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    await db.delete(post)
    await db.commit()

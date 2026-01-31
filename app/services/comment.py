from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.config.database import get_db
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentUpdate


async def get_all(post_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Post).where(Post.id == post_id))
    existing_post = result.scalars().first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    result = await db.execute(select(Comment).options(selectinload(Comment.user)).where(Comment.post_id == post_id))
    comments = result.scalars().all()
    return comments


async def get_by_id(post_id: UUID, comment_id: UUID, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == post_id))
    existing_post = result.scalars().first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    result = await db.execute(select(Comment).where(Comment.id == comment_id and Post.id == post_id))
    existing_comment = result.scalars().first()

    if not existing_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    return existing_comment


async def create(payload: CommentCreate, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == payload.post_id))
    existing_post = result.scalars().first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    new_comment = Comment(content=payload.content,
                          post_id=payload.post_id, user_id=payload.user_id)

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


async def update(payload: CommentUpdate, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == payload.post_id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    result = await db.execute(select(Comment).where(Comment.id == payload.id and Post.id == payload.post_id))
    comment = result.scalars().first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment.user_id != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(comment, field, value)

    await db.commit()
    await db.refresh(comment)
    return comment

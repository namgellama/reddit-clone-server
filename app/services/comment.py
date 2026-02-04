from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate, CommentUpdate
from app.services import post as post_service


# Get all
async def get_all(post_id: UUID, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == post_id))
    existing_post = result.scalars().first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    result = await db.execute(
        select(Comment)
        .options(selectinload(Comment.user))
        .where(Comment.post_id == post_id)
    )
    comments = result.scalars().all()
    return comments


# Get by id
async def get_by_id(id: UUID, db: AsyncSession):
    result = await db.execute(select(Comment).where(Comment.id == id))
    existing_comment = result.scalars().first()

    if not existing_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    return existing_comment


# Get by post id and comment id
async def get_by_post_id_and_comment_id(
    post_id: UUID, comment_id: UUID, db: AsyncSession
):
    await post_service.get_by_id(id=post_id)

    result = await db.execute(
        select(Comment).where((Comment.id == comment_id) & (Post.id == post_id))
    )
    existing_comment = result.scalars().first()

    if not existing_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    return existing_comment


# Create
async def create(payload: CommentCreate, db: AsyncSession):
    await post_service.get_by_id(id=payload.post_id, db=db)

    new_comment = Comment(
        content=payload.content, post_id=payload.post_id, user_id=payload.user_id
    )

    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


# Update
async def update(payload: CommentUpdate, db: AsyncSession):
    comment = await get_by_post_id_and_comment_id(
        post_id=payload.post_id, comment_id=payload.id, db=db
    )

    if comment.user_id != payload.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(comment, field, value)

    await db.commit()
    await db.refresh(comment)
    return comment


# Delete
async def delete(post_id: UUID, comment_id: UUID, user_id: UUID, db: AsyncSession):
    comment = await get_by_post_id_and_comment_id(
        post_id=post_id, comment_id=comment_id, db=db
    )

    if comment.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    await db.delete(comment)
    await db.commit()

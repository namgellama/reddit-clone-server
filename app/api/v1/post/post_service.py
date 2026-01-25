from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.config.database import get_db
from app.api.v1.post.post_model import Post
from app.api.v1.post.post_schema import PostCreate


async def get_all(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Post).options(selectinload(Post.author)))
    posts = result.scalars().all()
    return posts


async def get_by_id(id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Post).options(selectinload(Post.author)).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    return post


async def create(payload: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    new_post = Post(title=payload.title,
                    content=payload.content, user_id=payload.user_id)

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=['author'])
    return new_post


async def update(id: UUID, payload: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    if post.user_id != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")

    post.title = payload.title
    post.content = payload.content
    post.user_id = payload.user_id

    await db.commit()
    await db.refresh(post, attribute_names=['author'])
    return post


async def delete(id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    await db.delete(post)
    await db.commit()

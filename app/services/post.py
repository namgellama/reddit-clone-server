from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

# Get all


async def get_all(db: AsyncSession):
    result = await db.execute(select(Post).options(selectinload(Post.author)))
    posts = result.scalars().all()
    return posts

# Get by id


async def get_by_id(id: UUID, db: AsyncSession):
    result = await db.execute(select(Post).options(selectinload(Post.author)).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    return post

# Create


async def create(payload: PostCreate, db: AsyncSession):
    new_post = Post(title=payload.title,
                    content=payload.content, user_id=payload.user_id)

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=['author'])
    return new_post

# Update


async def update(payload: PostUpdate, db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == payload.id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    if post.user_id != payload.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    post.title = payload.title
    post.content = payload.content
    post.user_id = payload.user_id

    await db.commit()
    await db.refresh(post, attribute_names=['author'])
    return post

# Delete


async def delete(id: UUID, user_id: UUID,  db: AsyncSession):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    await db.delete(post)
    await db.commit()

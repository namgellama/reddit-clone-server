from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate


def get_all(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Post))
    posts = result.scalars().all()
    return posts


def get_by_id(id: UUID, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    return post


def create(payload: PostCreate, db: Annotated[Session, Depends(get_db)]):
    new_post = Post(title=payload.title, content=payload.content)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def update(id: UUID, payload: PostCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    post.title = payload.title,
    post.content = payload.content

    db.commit()
    db.refresh(post)
    return post

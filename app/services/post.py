from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.post import Post


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

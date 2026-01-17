from typing import Annotated

from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.post import Post


def get_all(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(Post))
    posts = result.scalars().all()
    return posts

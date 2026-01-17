from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post import PostResponse
from app.services import post


router = APIRouter()


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    return post.get_all(db)


@router.get("/{id}", response_model=PostResponse)
def get_post(id: UUID, db: Annotated[Session, Depends(get_db)]):
    return post.get_by_id(id=id, db=db)

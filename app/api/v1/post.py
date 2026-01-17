from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.post import PostResponse, PostCreate
from app.services import post


router = APIRouter()


@router.get("/", response_model=list[PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    return post.get_all(db)


@router.get("/{id}", response_model=PostResponse)
def get_post(id: UUID, db: Annotated[Session, Depends(get_db)]):
    return post.get_by_id(id=id, db=db)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(body: PostCreate, db: Annotated[Session, Depends(get_db)]):
    return post.create(payload=body, db=db)

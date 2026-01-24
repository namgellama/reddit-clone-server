from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.post import PostResponse, PostCreate
from app.services import post


router = APIRouter()


@router.get("/", response_model=list[PostResponse])
async def get_posts(db: Annotated[AsyncSession, Depends(get_db)]):
    return await post.get_all(db)


@router.get("/{id}", response_model=PostResponse)
async def get_post(id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    return await post.get_by_id(id=id, db=db)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(body: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await post.create(payload=body, db=db)


@router.put("/{id}", response_model=PostResponse)
async def update_post(id: UUID, body: PostCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await post.update(id=id, payload=body, db=db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: UUID,  db: Annotated[AsyncSession, Depends(get_db)]):
    return await post.delete(id=id,  db=db)

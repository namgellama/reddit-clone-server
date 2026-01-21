from typing import Annotated

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserResponse, UserCreate
from app.services import user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[UserResponse, Depends(user.get_current_user)]):
    return current_user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return user.create(payload=body, db=db)

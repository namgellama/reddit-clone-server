from typing import Annotated

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.user import UserResponse
from app.services import user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[UserResponse, Depends(user.get_current_user)]):
    return current_user

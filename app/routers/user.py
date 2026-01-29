from typing import Annotated

from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.config.database import get_db
from app.api.v1.user.user_schema import UserResponse
from app.api.v1.user import user_service

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[UserResponse, Depends(user_service.get_current_user)]):
    return current_user

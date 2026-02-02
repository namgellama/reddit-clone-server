from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.user import UserResponse
from app.services.user import get_current_user

router = APIRouter()


"""
    @desc Get current user
    @route GET /api/v1/users/me
    @access Private

"""


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return current_user

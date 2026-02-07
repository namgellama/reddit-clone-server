from fastapi import APIRouter

from app.utils.security import CurrentUser
from app.schemas.user import UserResponse

router = APIRouter()


"""
    @desc Get current user
    @route GET /api/v1/users/me
    @access Private

"""


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser):
    return current_user

from typing import Annotated

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserResponse, UserCreate
from app.services import user

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, db: Annotated[Session, Depends(get_db)]):
    return user.create(payload=body, db=db)

from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginResponse
from app.database import get_db
from app.services import auth

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    return await auth.login(form_data=form_data, db=db, response=response)

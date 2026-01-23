from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginResponse, RegisterEmail
from app.schemas.general import SimpleResponse
from app.config.database import get_db
from app.services import auth

router = APIRouter()


@router.post("/register-email", response_model=SimpleResponse)
async def register_email(body: RegisterEmail,  db: Annotated[AsyncSession, Depends(get_db)]):
    await auth.register_email(payload=body, db=db)

    return SimpleResponse(
        success=True,
        message="Otp has been sent to your email."
    )


@router.post("/login", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    return await auth.login(form_data=form_data, db=db, response=response)

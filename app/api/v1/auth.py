from typing import Annotated

from fastapi import APIRouter, Depends,  Response, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginResponse, RegisterEmail, VerifyEmail
from app.schemas.general import SimpleResponse
from app.schemas.user import UserResponse, UserCreate
from app.config.database import get_db
from app.services import auth
from app.config.oauth import oauth
from app.config import env


router = APIRouter()


@router.post("/register-email", response_model=SimpleResponse)
async def register_email(body: RegisterEmail,  db: Annotated[AsyncSession, Depends(get_db)]):
    await auth.register_email(payload=body, db=db)

    return SimpleResponse(
        success=True,
        message="Otp has been sent to your email."
    )


@router.post("/verify-email", response_model=SimpleResponse)
async def register_email(body: VerifyEmail,  db: Annotated[AsyncSession, Depends(get_db)]):
    match = await auth.verify_email(payload=body, db=db)

    if match:
        return SimpleResponse(
            success=True,
            message="Your email is verified successfully"
        )

    return SimpleResponse(
        success=False,
        message="OTP does not match"
    )


@router.post("/register", response_model=UserResponse)
async def register_user(body: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await auth.register_user(payload=body, db=db)


@router.post("/login", response_model=LoginResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    return await auth.login(form_data=form_data, db=db, response=response)


@router.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, env.GOOGLE_REDIRECT_URI)


@router.get("/google/callback")
async def auth_google(request: Request, db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    data = await auth.google_callback(request=request, db=db, response=response)

    return RedirectResponse(url=f"{env.FRONTEND_URL}/auth?access_token={data['access_token']}")


@router.post("/logout", response_model=SimpleResponse)
def logout(response: Response):
    auth.logout(response=response)

    return SimpleResponse(
        success=True,
        message="You have been logged out successfully"
    )

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginResponse, RegisterEmail, VerifyEmail, Token
from app.schemas.response import SimpleApiResponse
from app.schemas.user import UserResponse, UserCreate
from app.database.db import get_db
from app.services import auth as auth_service
from app.config.oauth import oauth
from app.config.env import settings
from app.utils.cookie import set_cookie


router = APIRouter()


"""
    @desc Register email
    @route POST /api/v1/auth/register-email
    @access Public

"""


@router.post("/register-email", response_model=SimpleApiResponse)
async def register_email(
    body: RegisterEmail, db: Annotated[AsyncSession, Depends(get_db)]
):
    await auth_service.register_email(payload=body, db=db)

    return {"message": "Otp has been sent to your email."}


"""
    @desc Verify email
    @route POST /api/v1/auth/verify-email
    @access Public

"""


@router.post("/verify-email", response_model=SimpleApiResponse)
async def verify_email(body: VerifyEmail, db: Annotated[AsyncSession, Depends(get_db)]):
    match = await auth_service.verify_email(payload=body, db=db)

    if not match:
        raise HTTPException(status_code=400, detail="OTP does not match")

    return {"message": "Your email is verified successfully"}


"""
    @desc Register user
    @route POST /api/v1/auth/register
    @access Public

"""


@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(body: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await auth_service.register_user(payload=body, db=db)


"""
    @desc Login user
    @route POST /api/v1/auth/login
    @access Public

"""


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
    response: Response,
):
    access_token = await auth_service.login(
        form_data=form_data, db=db, response=response
    )

    return Token(access_token=access_token, token_type="bearer")


"""
    @desc Login with google
    @route POST /api/v1/auth/google
    @access Public

"""


@router.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, settings.google_redirect_uri)


"""
    @desc Google callback
    @route POST /api/v1/auth/google/callback
    @access Public

"""


@router.get("/google/callback")
async def auth_google(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    data = await auth_service.google_callback(request=request, db=db)

    redirect_response = RedirectResponse(
        url=f"{settings.frontend_url}/google/callback?access_token={data['access_token']}"
    )

    set_cookie(
        response=redirect_response,
        key="access_token",
        value=data["access_token"],
        max_age=60 * 30,
    )
    set_cookie(
        response=redirect_response,
        key="refresh_token",
        value=data["refresh_token"],
        max_age=60 * 60 * 24 * 7,
    )

    return redirect_response


"""
    @desc Logout user
    @route POST /api/v1/auth/logout
    @access Public

"""


@router.post("/logout", response_model=SimpleApiResponse)
def logout(response: Response):
    auth_service.logout(response=response)

    return {"message": "You have been logged out successfully"}


"""
    @desc Refresh token
    @route POST /api/v1/auth/refresh-token
    @access Private

"""


@router.post("/refresh-token", response_model=LoginResponse)
async def refresh_token(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    return await auth_service.refresh_token(request=request, db=db)

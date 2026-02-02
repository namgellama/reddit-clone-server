from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,  Response, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import LoginResponse, RegisterEmail, VerifyEmail, Token
from app.schemas.response import APIResponse
from app.schemas.user import UserResponse, UserCreate
from app.config.database import get_db
from app.services import auth as auth_service
from app.config.oauth import oauth
from app.config import env


router = APIRouter()


"""
    @desc Register email
    @route POST /api/v1/auth/register-email
    @access Public

"""


@router.post("/register-email", response_model=APIResponse[None])
async def register_email(body: RegisterEmail,  db: Annotated[AsyncSession, Depends(get_db)]):
    await auth_service.register_email(payload=body, db=db)

    return APIResponse(
        success=True,
        message="Otp has been sent to your email.",
        data=None
    )


"""
    @desc Verify email
    @route POST /api/v1/auth/verify-email
    @access Public

"""


@router.post("/verify-email", response_model=APIResponse[None])
async def register_email(body: VerifyEmail,  db: Annotated[AsyncSession, Depends(get_db)]):
    match = await auth_service.verify_email(payload=body, db=db)

    if not match:
        raise HTTPException(status_code=400, detail="OTP does not match")

    return APIResponse(
        success=True,
        message="Your email is verified successfully",
        data=None
    )


"""
    @desc Register user
    @route POST /api/v1/auth/register
    @access Public

"""


@router.post("/register", response_model=APIResponse[UserResponse], status_code=201)
async def register_user(body: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    new_user = await auth_service.register_user(payload=body, db=db)

    return APIResponse(
        success=True,
        message="User registered successfully",
        data=new_user
    )


"""
    @desc Login user
    @route POST /api/v1/auth/login
    @access Public

"""


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    access_token = await auth_service.login(form_data=form_data, db=db, response=response)

    return Token(
        access_token=access_token,
        token_type="bearer"
    )


"""
    @desc Login with google
    @route POST /api/v1/auth/google
    @access Public

"""


@router.get("/google")
async def login_google(request: Request):
    return await oauth.google.authorize_redirect(request, env.GOOGLE_REDIRECT_URI)


"""
    @desc Google callback
    @route POST /api/v1/auth/google/callback
    @access Public

"""


@router.get("/google/callback")
async def auth_google(request: Request, db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    data = await auth_service.google_callback(request=request, db=db, response=response)

    return RedirectResponse(url=f"{env.FRONTEND_URL}/auth?access_token={data['access_token']}")


"""
    @desc Logout user
    @route POST /api/v1/auth/logout
    @access Public

"""


@router.post("/logout", response_model=APIResponse[None])
def logout(response: Response):
    auth_service.logout(response=response)

    return APIResponse(
        success=True,
        message="You have been logged out successfully",
        data=None
    )


"""
    @desc Refresh token
    @route POST /api/v1/auth/refresh-token
    @access Private

"""


@router.post("/refresh-token", response_model=APIResponse[LoginResponse])
async def refresh_token(request: Request, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    access_token = await auth_service.refresh_token(request=request, response=response, db=db)

    return APIResponse(
        success=True,
        message="Token refreshed successfully",
        data=access_token
    )

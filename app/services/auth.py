from typing import Annotated
from fastapi import Depends,  HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from authlib.integrations.base_client import OAuthError
from authlib.oauth2.rfc6749 import OAuth2Token
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.user import User
from app.utils.security import verify_password, create_token, decode_token
from app.utils.cookie import set_cookie, delete_cookie
from app.schemas.auth import RegisterEmail, VerifyEmail, GoogleUser
from app.schemas.user import UserCreate
from app.utils import mail
from app.utils.otp import generate_otp, store_otp, verify_otp
from app.config.oauth import oauth

from . import user as user_service


# Register email
async def register_email(payload: RegisterEmail, db: Annotated[AsyncSession, Depends(get_db)]):
    existing_email = await user_service.get_user_by_email(email=payload.email, db=db)

    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    otp = generate_otp()
    await store_otp(f"otp:{payload.email}", 300, otp)

    await mail.send_mail(
        subject="Verify your email",
        recipients=[payload.email],
        body=f"""
             <h2>Email Verification</h2>
                <p>Your OTP:</p>
                <h1>{otp}</h1>
                <p>Expires in 10 minutes.</p>
        """
    )


# Verify email
async def verify_email(payload: VerifyEmail, db: Annotated[AsyncSession, Depends(get_db)]):
    existing_email = await user_service.get_user_by_email(email=payload.email, db=db)

    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    return await verify_otp(name=f"otp:{payload.email}", otp=payload.otp)


# Register user
async def register_user(payload: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await user_service.create(payload=payload, db=db)


# Login
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password):
        raise credentials_exception

    access_token = create_token(
        data={"sub": str(user.id)}, type="access"
    )
    refresh_token = create_token(
        data={"sub": str(user.id)}, type="refresh"
    )

    set_cookie(response=response, key="refresh_token",
               value=refresh_token, max_age=60*60*24*7)

    return access_token


# Google callback
async def google_callback(request, db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    try:
        user_response: OAuth2Token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Google token")

    user_info = user_response.get("userinfo")

    google_user = GoogleUser(**user_info)

    existing_user = await user_service.get_user_by_google_sub(str(google_user.sub), db)

    if existing_user:
        db_user = existing_user
    else:
        new_user = UserCreate(
            username=google_user.email.split("@")[0],
            email=google_user.email,
            password=None,
            google_sub=str(google_user.sub)
        )

        db_user = await user_service.create(new_user, db)

    access_token = create_token(
        data={"sub": str(db_user.id)}, type="access"
    )
    refresh_token = create_token(
        data={"sub": str(db_user.id)}, type="refresh"
    )

    set_cookie(response=response, key="refresh_token",
               value=refresh_token, max_age=60*60*24*7)

    return {"access_token": access_token}


# Logout
def logout(response: Response):
    delete_cookie(response=response, key="refresh_token")


# Refresh token
async def refresh_token(request: Request, response: Response, db: Annotated[AsyncSession, Depends(get_db)]):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token found"
        )

    payload = decode_token(token=refresh_token, type="refresh")

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    db_user = await user_service.get_user_by_id(id=payload, db=db)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )

    access_token = create_token(
        data={"sub": str(db_user.id)}, type="access"
    )

    return {"access_token": access_token}

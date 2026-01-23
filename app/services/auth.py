from typing import Annotated

from fastapi import Depends,  HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.user import User
from app.utils.password import verify_password
from app.utils.jwt import create_token
from app.utils.cookie import set_cookie
from app.schemas.auth import RegisterEmail
from app.schemas.user import UserCreate
from app.services import user
from app.utils.otp import generate_otp, store_otp


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def register_email(payload: RegisterEmail, db: Annotated[AsyncSession, Depends(get_db)]):
    existing_email = await user.get_user_by_email(email=payload.email, db=db)

    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    otp = generate_otp()
    await store_otp(f"otp:{payload.email}", 300, otp)

    return {
        "success": True,
        "message": "Otp has been sent to your email"
    }


async def register(payload: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await user.create(payload=payload, db=db)


async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[AsyncSession, Depends(get_db)], response: Response):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user:
        raise credentials_exception

    if not verify_password(form_data.password, user.password):
        raise credentials_exception

    access_token = create_token(
        data={"sub": str(user.id)}, type="access"
    )
    refresh_token = create_token(
        data={"sub": str(user.id)}, type="refresh"
    )

    set_cookie(response=response, key="refresh_token",
               value=refresh_token, max_age=60*60*24*7)

    return {"access_token": access_token}

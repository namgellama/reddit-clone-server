from typing import Literal, Annotated, Optional
from datetime import datetime, timedelta, timezone
import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.config.env import settings
from app.schemas.user import UserResponse
from app.database.db import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login", auto_error=False
)

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


def create_token(data: dict, type: Literal["access", "refresh"]):
    to_encode = data.copy()

    if type == "access":
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        secret_key = settings.jwt_access_secret
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        secret_key = settings.jwt_refresh_secret

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, secret_key.get_secret_value(), algorithm="HS256"
    )
    return encoded_jwt


def decode_token(token: str, type: Literal["access", "refresh"]):
    if type == "access":
        secret_key = settings.jwt_access_secret
    else:
        secret_key = settings.jwt_refresh_secret

    try:
        payload = jwt.decode(token, secret_key.get_secret_value(), algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        id = decode_token(token, "access")

        if id is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == id))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]


async def get_optional_current_user(
    token: Annotated[Optional[str], Depends(optional_oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    if not token:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        id = decode_token(token, "access")

        if id is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == id))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
    return user


OptionalCurrentUser = Annotated[
    Optional[UserResponse], Depends(get_optional_current_user)
]

from typing import Literal, Annotated
from datetime import datetime, timedelta, timezone
import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.config import env
from app.schemas.user import UserResponse
from app.config.database import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


def create_token(data: dict, type: Literal["access", "refresh"]):
    to_encode = data.copy()

    if type == "access":
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        secret_key = env.JWT_ACCESS_SECRET
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        secret_key = env.JWT_REFRESH_SECRET

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str, type: Literal["access", "refresh"]):
    if type == "access":
        secret_key = env.JWT_ACCESS_SECRET
    else:
        secret_key = env.JWT_REFRESH_SECRET

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
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

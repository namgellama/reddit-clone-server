from typing import Annotated

from fastapi import Depends, HTTPException, status

from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from jwt.exceptions import InvalidTokenError

from app.schemas.user import UserCreate
from app.database import get_db
from app.models.user import User
from app.utils.password import hash_password
from app.utils.jwt import decode_token
from app.services.auth import oauth2_scheme


async def get_user_by_email(email: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    return user


async def get_user_by_username(username: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[AsyncSession, Depends(get_db)]):
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


async def create(payload: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.username == payload.username))
    existingUsername = result.scalars().first()

    if existingUsername:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Username already exists")

    result = await db.execute(select(User).where(User.email == payload.email))
    existingEmail = result.scalars().first()

    if existingEmail:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    if payload.password:
        payload.password = hash_password(payload.password)

    new_user = User(username=payload.username,
                    email=payload.email, password=payload.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

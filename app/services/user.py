from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from app.schemas.user import UserCreate
from app.config.database import get_db
from app.models.user import User
from app.utils.security import hash_password, decode_token, oauth2_scheme


# Get user by id
async def get_by_id(id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalars().first()

    return user


# Get user by email
async def get_by_email(email: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    return user


# Get user by username
async def get_by_username(username: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    return user


# Get user by google sub
async def get_by_google_sub(
    google_sub: str, db: Annotated[AsyncSession, Depends(get_db)]
):
    print("googele_sub", google_sub)
    result = await db.execute(select(User).where(User.google_sub == google_sub))
    user = result.scalars().first()

    return user


# Get current user
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

    user = await get_by_id(id=id, db=db)

    if user is None:
        raise credentials_exception
    return user


# Create
async def create(payload: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    username = await get_by_username(username=payload.username, db=db)

    if username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )

    email = await get_by_email(email=payload.email)

    if email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    if payload.password:
        payload.password = hash_password(payload.password)

    new_user = User(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        google_sub=payload.google_sub,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

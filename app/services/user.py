from typing import Annotated

from fastapi import Depends, HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate
from app.database import get_db
from app.models.user import User
from app.utils.password import hash_password


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

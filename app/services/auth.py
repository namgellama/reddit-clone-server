from typing import Annotated

from fastapi import Depends,  HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.utils.password import verify_password
from app.utils.jwt import create_token
from app.utils.cookie import set_cookie


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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

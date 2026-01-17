
from typing import Optional, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, EmailStr, constr


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120,)


class UserCreate(UserBase):
    password: Optional[Annotated[str, Field(min_length=1)]] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

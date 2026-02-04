from typing import Optional, Annotated
from uuid import UUID
import re
from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=120)


class UserCreate(UserBase):
    password: Optional[Annotated[str, Field(min_length=1)]] = None
    google_sub: Optional[Annotated[str, Field(min_length=1)]] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]):
        if v is None:
            return v  # allow null password

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one symbol")

        return v


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

from .user import UserResponse


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: UUID


class PostUpdate(PostCreate):
    id: UUID


class Count(BaseModel):
    comment: int
    upvote: int
    downvote: int


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date_posted: datetime
    user_id: UUID
    author: UserResponse


class PostResponseWithCount(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date_posted: datetime
    user_id: UUID
    count: Count
    author: UserResponse

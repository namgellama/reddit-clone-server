from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from .user import UserResponse


class CommentBase(BaseModel):
    content: str = Field(min_length=1)


class CommentCreate(CommentBase):
    user_id: UUID
    post_id: UUID


class CommentUpdate(CommentCreate):
    id: UUID


class CommentCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
    user: UserResponse
    post_id: UUID
    parent_id: UUID | None


class CommentResponse(CommentCreateResponse):
    score: int
    user_vote: str | None

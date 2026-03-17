from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict, model_validator

from .user import UserResponse


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class PostCreate(PostBase):
    user_id: UUID
    images: list[str] = Field(default_factory=list, max_length=3)


class PostUpdate(BaseModel):
    id: UUID
    title: str | None = Field(min_length=1, max_length=100, default=None)
    content: str | None = Field(min_length=1, default=None)
    images: list[str] | None = Field(default=None, max_length=3)
    previous_images: list[str] | None = Field(default=None, max_length=3)
    user_id: UUID

    @model_validator(mode="after")
    def validate_total_images(self):
        total = len(self.images or []) + len(self.previous_images or [])

        if total > 3:
            raise ValueError("Total images cannot exceed 3")

        return self


class Count(BaseModel):
    comment: int
    upvote: int
    downvote: int


class PostCreateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    content: str
    images: list[str]
    date_posted: datetime
    user: UserResponse


class PostResponse(PostCreateResponse):
    score: int
    user_vote: str | None
    comment_count: int

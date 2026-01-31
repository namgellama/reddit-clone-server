from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class CommentBase(BaseModel):
    content: str = Field(min_length=1)


class CommentResponse(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    user_id: UUID
    post_id: UUID
    parent_id: UUID | None

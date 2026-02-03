from pydantic import BaseModel, model_validator, ConfigDict
from uuid import UUID
from datetime import datetime


class UpvoteBase(BaseModel):
    post_id: UUID | None = None
    comment_id: UUID | None = None


class UpvoteCreate(UpvoteBase):
    user_id: UUID

    @model_validator(mode="after")
    def validate_target(self):
        if self.post_id is None and self.comment_id is None:
            raise ValueError("Either post_id or comment_id must be provided")

        if self.post_id is not None and self.comment_id is not None:
            raise ValueError("Only one of post_id or comment_id is allowed")

        return self


class UpvoteCreateResponse(UpvoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime


class UpvoteResponse(BaseModel):
    upvoted: bool

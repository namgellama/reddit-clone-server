from uuid import UUID
from pydantic import BaseModel


class UpvoteBase(BaseModel):
    user_id: UUID


class PostUpvoteCreate(UpvoteBase):
    post_id: UUID


class UpvoteResponse(BaseModel):
    upvoted: bool
    message: str

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date_posted: datetime

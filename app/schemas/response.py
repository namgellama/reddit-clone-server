from pydantic import BaseModel


class SimpleApiResponse(BaseModel):
    message: str


class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    has_more: bool

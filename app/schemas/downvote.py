from pydantic import BaseModel


class DownvoteResponse(BaseModel):
    downvoted: bool
    message: str

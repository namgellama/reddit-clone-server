from pydantic import BaseModel


class UpvoteResponse(BaseModel):
    upvoted: bool
    message: str

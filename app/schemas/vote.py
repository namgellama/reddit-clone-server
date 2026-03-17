from pydantic import BaseModel

from app.models.vote import VoteType


class VoteRequest(BaseModel):
    type: VoteType


class VoteResponse(BaseModel):
    vote_type: VoteType | None
    score: int

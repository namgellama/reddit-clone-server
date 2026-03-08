from pydantic import BaseModel


class SimpleApiResponse(BaseModel):
    message: str

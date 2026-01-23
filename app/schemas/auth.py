from pydantic import BaseModel, Field, EmailStr


class RegisterEmail(BaseModel):
    email: EmailStr = Field(max_length=120)


class RegisterEmailResponse(BaseModel):
    success: bool
    message: str


class LoginResponse(BaseModel):
    access_token: str

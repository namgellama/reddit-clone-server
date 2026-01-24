from pydantic import BaseModel, Field, EmailStr


class RegisterEmail(BaseModel):
    email: EmailStr = Field(max_length=120)


class VerifyEmail(RegisterEmail):
    otp: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")


class LoginResponse(BaseModel):
    access_token: str

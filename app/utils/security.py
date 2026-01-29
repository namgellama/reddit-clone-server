from typing import Literal
from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer


from app.config import env


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


def create_token(data: dict, type: Literal["access", "refresh"]):
    to_encode = data.copy()

    if type == "access":
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        secret_key = env.JWT_ACCESS_SECRET
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        secret_key = env.JWT_REFRESH_SECRET

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str, type: Literal["access", "refresh"]):
    if type == "access":
        secret_key = env.JWT_ACCESS_SECRET
    else:
        secret_key = env.JWT_REFRESH_SECRET

    print("token", token)

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")

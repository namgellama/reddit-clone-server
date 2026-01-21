from datetime import datetime, timedelta, timezone

import jwt

from app.config import JWT_SECRET_KEY


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str):
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    return payload.get("sub")

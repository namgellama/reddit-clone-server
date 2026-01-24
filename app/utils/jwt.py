from typing import Literal
from datetime import datetime, timedelta, timezone

import jwt

from app.config import env


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

    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    return payload.get("sub")

from fastapi import Response

from app.config.env import settings


def set_cookie(response: Response, key: str, value: str, max_age: int):
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=settings.env == "production",
        samesite="lax",
        max_age=max_age,
    )


def delete_cookie(response: Response, key: str):
    response.delete_cookie(
        key=key, httponly=True, secure=settings.env == "production", samesite="lax"
    )

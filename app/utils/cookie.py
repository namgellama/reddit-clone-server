from fastapi import Response

from app.config import ENV


def set_cookie(response: Response, key: str, value: str, max_age: int):
    response.set_cookie(key=key, value=value, httponly=True,
                        secure=ENV == "production", samesite="lax", max_age=max_age)

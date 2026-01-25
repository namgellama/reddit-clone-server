
import random

from app.shared.config.redis import redis_client


def generate_otp():
    return str(random.randint(100000, 999999))


async def store_otp(name: str, time: int, value: str):
    await redis_client.setex(name, time, value)


async def verify_otp(name: str, otp: str):
    stored_otp = await redis_client.get(name)
    return stored_otp == otp

import redis.asyncio as redis

from app.config import env

redis_client = redis.from_url(env.REDIS_URL, decode_responses=True)

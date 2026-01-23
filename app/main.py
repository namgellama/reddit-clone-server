from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.config.database import Base, engine
from app.api.v1 import post, user, auth
from app.services.redis import redis_client


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        await redis_client.ping()
        print("✅ Redis connected")
    except Exception as e:
        print("❌ Redis connection failed:", e)
        raise RuntimeError("Redis is required to start the app")

    yield

    # Shutdown
    await engine.dispose()
    await redis_client.close()
    print("🛑 Shutdown complete")

app = FastAPI(lifespan=lifespan)


@app.get('/')
def index():
    return {"message": "Hello World"}


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["User"])
app.include_router(post.router,  prefix="/api/v1/posts", tags=["Post"])

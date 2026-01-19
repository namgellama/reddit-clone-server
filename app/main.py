from fastapi import FastAPI

from contextlib import asynccontextmanager

from .database import Base, engine
from .api.v1 import post, user


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)


@app.get('/')
def index():
    return {"message": "Hello World"}


app.include_router(post.router,  prefix="/api/v1/posts", tags=["Post"])
app.include_router(user.router, prefix="/api/v1/users", tags=["User"])

from fastapi import FastAPI

from .database import Base, engine
from .api.v1 import post


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def index():
    return {"message": "Hello World"}


app.include_router(post.router, prefix="/posts", tags=["Post"])

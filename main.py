from fastapi import FastAPI

from database import Base, engine, get_db


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def index():
    return {"message": "Hello World"}

import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")

DATABASE_URL = os.getenv("DATABASE_URL")

JWT_ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")

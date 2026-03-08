from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from app.config.env import settings


config_data = {
    "GOOGLE_CLIENT_ID": settings.google_client_id,
    "GOOGLE_CLIENT_SECRET": settings.google_client_secret,
}

oauth = OAuth(Config(environ=config_data))

oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

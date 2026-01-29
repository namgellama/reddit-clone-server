from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from app.config import env


config_data = {'GOOGLE_CLIENT_ID': env.GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': env.GOOGLE_CLIENT_SECRET}

oauth = OAuth(Config(environ=config_data))

oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

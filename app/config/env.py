from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Environment
    env: str
    frontend_url: str
    secret_key: SecretStr

    # Database
    database_url: str

    # Jwt
    jwt_access_secret: SecretStr
    jwt_refresh_secret: SecretStr

    # Redis
    redis_url: str

    # Mail
    mail_username: str
    mail_password: SecretStr

    # Google Oauth
    google_client_id: str
    google_client_secret: SecretStr
    google_redirect_uri: str

    # Image file
    max_upload_size_bytes: int = 5 * 1024 * 1024  # 5 MB
    max_upload_length: int = 3


settings = Settings()  # type: ignore

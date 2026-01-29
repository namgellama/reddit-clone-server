from fastapi_mail import ConnectionConfig

from app.shared.config import env

conf = ConnectionConfig(
    MAIL_USERNAME=env.MAIL_USERNAME,
    MAIL_PASSWORD=env.MAIL_PASSWORD,
    MAIL_FROM=env.MAIL_USERNAME,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

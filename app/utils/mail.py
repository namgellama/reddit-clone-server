from pydantic import EmailStr
from fastapi_mail import FastMail, MessageSchema

from app.config.mail import conf


async def send_mail(subject: str, recipients: list[EmailStr], body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)

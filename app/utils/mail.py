from fastapi_mail import FastMail, MessageSchema, MessageType, NameEmail

from app.config.mail import conf


async def send_mail(subject: str, recipients: list[NameEmail], body: str):
    message = MessageSchema(
        subject=subject, recipients=recipients, body=body, subtype=MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(message)

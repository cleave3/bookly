from fastapi import Path
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from .config import Config

BASE_DIR = ""  # Path(__file__).resolve().parent

email_config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM_EMAIL,
    MAIL_PORT=465,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)

mail = FastMail(config=email_config)


def create_message(recipients: list[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipients, subject=subject, body=body, subtype=MessageType.html
    )
    return message

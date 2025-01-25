from celery import Celery
from src.mail import mail, create_message
from asgiref.sync import async_to_sync
from .config import broker_url, result_backend

c_app = Celery()

# c_app.config_from_object("src.config")

c_app.conf.broker_url = broker_url
c_app.conf.result_backend = result_backend


@c_app.task(name="send_email")
def send_email(recipients: list[str], subject: str, body: str):

    message = create_message(recipients=recipients, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)
    print("Email sent")

from datetime import date
from decimal import Decimal

from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from banki.configuration import settings


class EmailClient:
    _fm: FastMail
    _scheduler: BackgroundTasks

    def __init__(self, background_tasks: BackgroundTasks) -> None:
        conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            MAIL_FROM=settings.MAIL_FROM,
            USE_CREDENTIALS=settings.USE_CREDENTIALS,
            VALIDATE_CERTS=settings.VALIDATE_CERTS,
        )
        self._fm = FastMail(conf)
        self._scheduler = background_tasks

    def send_charge_email(self, email: str, name: str, amount: Decimal, due_date: date) -> None:
        message = MessageSchema(
            subject='Your charge just arrived!',
            recipients=[email],
            body=f"""
Hello {name}, you are being charged!

AMOUNT: $ {amount}
DUE DATE: {due_date}

Thanks.""".strip(),
            subtype=MessageType.plain,
        )
        self._scheduler.add_task(self._fm.send_message, message)

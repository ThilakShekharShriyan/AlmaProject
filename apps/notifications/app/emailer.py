import smtplib
from email.message import EmailMessage
from typing import Protocol

import resend

from app.config import settings


class EmailSender(Protocol):
    def send(self, to: str, subject: str, body: str) -> None: ...


class SmtpEmailSender:
    def send(self, to: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = settings.smtp_from
        message["To"] = to
        message["Subject"] = subject
        message.set_content(body)
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as smtp:
            if settings.smtp_use_tls:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
            if settings.smtp_user and settings.smtp_password:
                smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.send_message(message)


class ResendEmailSender:
    def send(self, to: str, subject: str, body: str) -> None:
        resend.api_key = settings.resend_api_key
        resend.Emails.send(
            {
                "from": settings.smtp_from,
                "to": [to],
                "subject": subject,
                "text": body,
            }
        )


def default_sender() -> EmailSender:
    if settings.resend_api_key:
        return ResendEmailSender()
    return SmtpEmailSender()

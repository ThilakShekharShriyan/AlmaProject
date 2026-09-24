from app.config import settings
from app.worker import handle_event

EVENT = {
    "lead_id": "lead-1",
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "document_id": "doc-1",
}


class RecordingSender:
    def __init__(self):
        self.messages = []

    def send(self, to: str, subject: str, body: str) -> None:
        self.messages.append((to, subject, body))


class FailingSender:
    def send(self, to: str, subject: str, body: str) -> None:
        raise RuntimeError("smtp down")


def test_sends_two_emails():
    sender = RecordingSender()
    handle_event(EVENT, sender)
    assert len(sender.messages) == 2
    assert sender.messages[0][0] == "ada@example.com"
    assert sender.messages[1][0] == settings.attorney_notification_email


def test_email_failure_does_not_raise():
    handle_event(EVENT, FailingSender())


def test_attorney_email_sends_when_prospect_email_fails():
    class ProspectFails:
        def __init__(self):
            self.sent = []

        def send(self, to, subject, body):
            if to == "ada@example.com":
                raise RuntimeError("testing recipient only")
            self.sent.append(to)

    sender = ProspectFails()
    handle_event(EVENT, sender)
    assert sender.sent == [settings.attorney_notification_email]


def test_real_smtp_starts_tls_and_logs_in(monkeypatch):
    calls = []

    class FakeSmtp:
        def __init__(self, host, port, timeout):
            calls.append(("connect", host, port, timeout))

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def ehlo(self):
            calls.append("ehlo")

        def starttls(self):
            calls.append("starttls")

        def login(self, user, password):
            calls.append(("login", user, password))

        def send_message(self, message):
            calls.append(("send", message["To"]))

    monkeypatch.setattr("app.emailer.smtplib.SMTP", FakeSmtp)
    monkeypatch.setattr("app.emailer.settings.smtp_host", "smtp.gmail.com")
    monkeypatch.setattr("app.emailer.settings.smtp_port", 587)
    monkeypatch.setattr("app.emailer.settings.smtp_use_tls", True)
    monkeypatch.setattr("app.emailer.settings.smtp_user", "leads@gmail.com")
    monkeypatch.setattr("app.emailer.settings.smtp_password", "app-password")
    monkeypatch.setattr("app.emailer.settings.smtp_from", "leads@gmail.com")

    from app.emailer import SmtpEmailSender

    SmtpEmailSender().send("ada@example.com", "Hello", "Body")
    assert ("connect", "smtp.gmail.com", 587, 10) in calls
    assert "starttls" in calls
    assert ("login", "leads@gmail.com", "app-password") in calls
    assert ("send", "ada@example.com") in calls


def test_resend_sender_posts_text_email(monkeypatch):
    sent = {}

    def fake_send(payload):
        sent.update(payload)

    monkeypatch.setattr("app.emailer.settings.resend_api_key", "re_test")
    monkeypatch.setattr("app.emailer.settings.smtp_from", "onboarding@resend.dev")
    monkeypatch.setattr("app.emailer.resend.Emails.send", fake_send)

    from app.emailer import ResendEmailSender

    ResendEmailSender().send("ada@example.com", "Hello", "Body")
    assert sent == {
        "from": "onboarding@resend.dev",
        "to": ["ada@example.com"],
        "subject": "Hello",
        "text": "Body",
    }

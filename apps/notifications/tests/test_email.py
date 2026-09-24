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
    assert sender.messages[1][0] == "attorney@example.com"


def test_email_failure_does_not_raise():
    handle_event(EVENT, FailingSender())

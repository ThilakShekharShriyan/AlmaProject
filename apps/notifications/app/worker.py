import json
import logging
from typing import Any

from redis import Redis

from app.config import settings
from app.emailer import EmailSender, default_sender

logger = logging.getLogger(__name__)


def handle_event(event: dict[str, Any], sender: EmailSender) -> None:
    name = f"{event['first_name']} {event['last_name']}"
    messages = (
        (
            event["email"],
            "We received your application",
            f"Hello {name}, we received your resume and an attorney will be in touch.",
        ),
        (
            settings.attorney_notification_email,
            f"New lead: {name}",
            f"{name} <{event['email']}> submitted a resume. Lead id {event['lead_id']}.",
        ),
    )
    for to, subject, body in messages:
        try:
            sender.send(to, subject, body)
        except Exception:
            logger.exception("lead %s saved; email to %s failed", event.get("lead_id"), to)


def consume_one(sender: EmailSender | None = None) -> bool:
    mailer = sender or default_sender()
    item = Redis.from_url(settings.redis_url).lpop(settings.lead_event_key)
    if item is None:
        return False
    handle_event(json.loads(item), mailer)
    return True

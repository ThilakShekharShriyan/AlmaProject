import json
import logging
from typing import Any

from redis import Redis

from app.config import settings
from app.emailer import EmailSender, SmtpEmailSender

logger = logging.getLogger(__name__)


def handle_event(event: dict[str, Any], sender: EmailSender) -> None:
    name = f"{event['first_name']} {event['last_name']}"
    try:
        sender.send(
            event["email"],
            "We received your application",
            f"Hello {name}, we received your resume and an attorney will be in touch.",
        )
        sender.send(
            settings.attorney_notification_email,
            f"New lead: {name}",
            f"{name} <{event['email']}> submitted a resume. Lead id {event['lead_id']}.",
        )
    except Exception:
        logger.exception("lead %s saved; email send failed", event.get("lead_id"))


def consume_one(sender: EmailSender | None = None) -> bool:
    mailer = sender or SmtpEmailSender()
    item = Redis.from_url(settings.redis_url).lpop(settings.lead_event_key)
    if item is None:
        return False
    handle_event(json.loads(item), mailer)
    return True

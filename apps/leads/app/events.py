import json

from redis import Redis

from app.config import settings
from app.models import Lead


def publish_lead_submitted(lead: Lead) -> None:
    payload = {
        "lead_id": lead.id,
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "document_id": lead.document_id,
    }
    Redis.from_url(settings.redis_url).lpush(settings.lead_event_key, json.dumps(payload))

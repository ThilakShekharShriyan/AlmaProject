import json

import jwt
from fastapi.testclient import TestClient
from redis import Redis

from app.config import settings
from app.main import app

LEAD = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "document_id": "doc-1",
}


def auth_header() -> dict[str, str]:
    token = jwt.encode({"sub": "attorney@example.com"}, settings.jwt_secret, algorithm="HS256")
    return {"Authorization": f"Bearer {token}"}


def test_create_publishes_event():
    redis = Redis.from_url(settings.redis_url)
    redis.delete(settings.lead_event_key)
    with TestClient(app) as client:
        response = client.post("/leads", json=LEAD)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "PENDING"
    raw = redis.lpop(settings.lead_event_key)
    assert json.loads(raw)["lead_id"] == body["id"]


def test_lead_remains_when_publish_fails(monkeypatch):
    def boom(_lead):
        raise RuntimeError("redis down")

    monkeypatch.setattr("app.main.publish_lead_submitted", boom)
    with TestClient(app) as client:
        created = client.post("/leads", json={**LEAD, "email": "kept@example.com"})
        lead_id = created.json()["id"]
        fetched = client.get(f"/leads/{lead_id}", headers=auth_header())
    assert created.status_code == 201
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "PENDING"


def test_list_requires_auth():
    with TestClient(app) as client:
        response = client.get("/leads")
    assert response.status_code == 401


def test_repeat_reached_out_conflicts():
    with TestClient(app) as client:
        created = client.post(
            "/leads",
            json={**LEAD, "email": "grace@example.com"},
        )
        lead_id = created.json()["id"]
        headers = auth_header()
        first = client.patch(f"/leads/{lead_id}", json={"status": "REACHED_OUT"}, headers=headers)
        second = client.patch(f"/leads/{lead_id}", json={"status": "REACHED_OUT"}, headers=headers)
    assert first.status_code == 200
    assert second.status_code == 409

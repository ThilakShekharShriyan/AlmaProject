import json
from datetime import datetime, timezone

from fastapi import HTTPException
from fastapi.testclient import TestClient
from redis import Redis

from app.config import settings
from app.main import app

LEAD = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "document_id": "11111111-1111-1111-1111-111111111111",
}
AUTH = {"Authorization": "Bearer attorney-token"}


def row(body: dict, status: str = "PENDING") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    return {**body, "id": "22222222-2222-2222-2222-222222222222", "status": status, "created_at": now, "updated_at": now}


def test_create_publishes_event(monkeypatch):
    saved = row(LEAD)
    monkeypatch.setattr("app.main.insert_lead", lambda body: saved)
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
    saved = row({**LEAD, "email": "kept@example.com"})
    monkeypatch.setattr("app.main.insert_lead", lambda body: saved)

    def boom(_lead):
        raise RuntimeError("redis down")

    monkeypatch.setattr("app.main.publish_lead_submitted", boom)
    monkeypatch.setattr("app.main.get_lead", lambda lead_id, token: saved)
    with TestClient(app) as client:
        created = client.post("/leads", json={**LEAD, "email": "kept@example.com"})
        lead_id = created.json()["id"]
        fetched = client.get(f"/leads/{lead_id}", headers=AUTH)
    assert created.status_code == 201
    assert fetched.status_code == 200
    assert fetched.json()["status"] == "PENDING"


def test_list_requires_auth():
    with TestClient(app) as client:
        response = client.get("/leads")
    assert response.status_code == 401


def test_repeat_reached_out_conflicts(monkeypatch):
    pending = row({**LEAD, "email": "grace@example.com"})
    reached = {**pending, "status": "REACHED_OUT"}
    calls = {"n": 0}

    monkeypatch.setattr("app.main.insert_lead", lambda body: pending)

    def update(lead_id, token):
        calls["n"] += 1
        if calls["n"] > 1:
            raise HTTPException(status_code=409, detail="lead is already REACHED_OUT")
        return reached

    monkeypatch.setattr("app.main.update_status", update)
    with TestClient(app) as client:
        created = client.post("/leads", json={**LEAD, "email": "grace@example.com"})
        lead_id = created.json()["id"]
        first = client.patch(f"/leads/{lead_id}", json={"status": "REACHED_OUT"}, headers=AUTH)
        second = client.patch(f"/leads/{lead_id}", json={"status": "REACHED_OUT"}, headers=AUTH)
    assert first.status_code == 200
    assert second.status_code == 409

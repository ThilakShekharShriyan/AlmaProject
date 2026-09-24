from fastapi.testclient import TestClient

from app import main


def test_health_ok(monkeypatch):
    monkeypatch.setattr(main, "redis_ok", lambda: True)
    response = TestClient(main.app).get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "notifications"


def test_health_down(monkeypatch):
    def fail():
        raise RuntimeError("down")

    monkeypatch.setattr(main, "redis_ok", fail)
    response = TestClient(main.app).get("/health")
    assert response.status_code == 503

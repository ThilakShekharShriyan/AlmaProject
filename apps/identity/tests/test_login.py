from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app


def test_login_success(monkeypatch):
    monkeypatch.setattr("app.main.sign_in", lambda email, password: "supabase-token")
    with TestClient(app) as client:
        response = client.post("/auth/login", json={"email": "attorney@gmail.com", "password": "change-me"})
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"] == "supabase-token"


def test_login_rejects_bad_password(monkeypatch):
    def reject(email, password):
        raise HTTPException(status_code=401, detail="invalid credentials")

    monkeypatch.setattr("app.main.sign_in", reject)
    with TestClient(app) as client:
        response = client.post("/auth/login", json={"email": "attorney@gmail.com", "password": "not-the-password"})
    assert response.status_code == 401

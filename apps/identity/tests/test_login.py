from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def test_login_success():
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={"email": settings.attorney_email, "password": settings.attorney_password},
        )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_rejects_bad_password():
    with TestClient(app) as client:
        response = client.post(
            "/auth/login",
            json={"email": settings.attorney_email, "password": "not-the-password"},
        )
    assert response.status_code == 401

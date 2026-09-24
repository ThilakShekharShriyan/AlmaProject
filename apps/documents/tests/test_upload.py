import jwt
from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def test_rejects_wrong_type():
    with TestClient(app) as client:
        response = client.post(
            "/documents",
            files={"file": ("notes.txt", b"hello", "text/plain")},
        )
    assert response.status_code == 422


def test_rejects_oversize(monkeypatch):
    monkeypatch.setattr(settings, "max_upload_bytes", 4)
    with TestClient(app) as client:
        response = client.post(
            "/documents",
            files={"file": ("cv.pdf", b"12345", "application/pdf")},
        )
    assert response.status_code == 422


def test_download_requires_auth():
    with TestClient(app) as client:
        created = client.post(
            "/documents",
            files={"file": ("cv.pdf", b"%PDF-1.4", "application/pdf")},
        )
        document_id = created.json()["document_id"]
        missing = client.get(f"/documents/{document_id}")
        token = jwt.encode({"sub": "attorney@example.com"}, settings.jwt_secret, algorithm="HS256")
        allowed = client.get(f"/documents/{document_id}", headers={"Authorization": f"Bearer {token}"})
    assert created.status_code == 200
    assert missing.status_code == 401
    assert allowed.status_code == 200
    assert allowed.content == b"%PDF-1.4"

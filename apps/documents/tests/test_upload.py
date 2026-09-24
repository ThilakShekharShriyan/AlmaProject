from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def test_rejects_wrong_type():
    with TestClient(app) as client:
        response = client.post("/documents", files={"file": ("notes.txt", b"hello", "text/plain")})
    assert response.status_code == 422


def test_rejects_oversize(monkeypatch):
    monkeypatch.setattr(settings, "max_upload_bytes", 4)
    with TestClient(app) as client:
        response = client.post("/documents", files={"file": ("cv.pdf", b"12345", "application/pdf")})
    assert response.status_code == 422


def test_download_requires_auth(monkeypatch):
    saved = {}

    def save_document(document_id, filename, content_type, payload, suffix):
        saved["id"] = document_id
        saved["bytes"] = payload
        saved["filename"] = filename
        saved["content_type"] = content_type

    def fetch_document(document_id, token):
        if token != "attorney-token":
            from fastapi import HTTPException

            raise HTTPException(status_code=401, detail="not authenticated")
        return saved["bytes"], saved["filename"], saved["content_type"]

    monkeypatch.setattr("app.main.save_document", save_document)
    monkeypatch.setattr("app.main.fetch_document", fetch_document)
    with TestClient(app) as client:
        created = client.post("/documents", files={"file": ("cv.pdf", b"%PDF-1.4", "application/pdf")})
        document_id = created.json()["document_id"]
        missing = client.get(f"/documents/{document_id}")
        allowed = client.get(f"/documents/{document_id}", headers={"Authorization": "Bearer attorney-token"})
    assert created.status_code == 200
    assert missing.status_code == 401
    assert allowed.status_code == 200
    assert allowed.content == b"%PDF-1.4"

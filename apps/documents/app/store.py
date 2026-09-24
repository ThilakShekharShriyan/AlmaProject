import httpx
from fastapi import HTTPException

from app.config import settings


def headers(token: str | None = None) -> dict[str, str]:
    bearer = token or settings.supabase_anon_key
    return {
        "apikey": settings.supabase_anon_key,
        "authorization": f"Bearer {bearer}",
    }


def save_document(document_id: str, filename: str, content_type: str, payload: bytes, suffix: str) -> None:
    storage_path = f"{document_id}{suffix}"
    uploaded = httpx.post(
        f"{settings.supabase_url}/storage/v1/object/resumes/{storage_path}",
        headers={**headers(), "content-type": content_type},
        content=payload,
        timeout=20,
    )
    if uploaded.status_code >= 300:
        raise HTTPException(status_code=502, detail="resume upload failed")
    created = httpx.post(
        f"{settings.supabase_url}/rest/v1/documents",
        headers={**headers(), "content-type": "application/json", "prefer": "return=minimal"},
        json={
            "id": document_id,
            "filename": filename,
            "content_type": content_type,
            "storage_path": storage_path,
        },
        timeout=10,
    )
    if created.status_code >= 300:
        raise HTTPException(status_code=502, detail="resume record failed")


def fetch_document(document_id: str, token: str) -> tuple[bytes, str, str]:
    found = httpx.get(
        f"{settings.supabase_url}/rest/v1/documents",
        params={"id": f"eq.{document_id}", "select": "filename,content_type,storage_path"},
        headers={**headers(token), "accept": "application/json"},
        timeout=10,
    )
    if found.status_code == 401:
        raise HTTPException(status_code=401, detail="not authenticated")
    rows = found.json() if found.status_code < 300 else []
    if not rows:
        raise HTTPException(status_code=404, detail="document not found")
    row = rows[0]
    downloaded = httpx.get(
        f"{settings.supabase_url}/storage/v1/object/resumes/{row['storage_path']}",
        headers=headers(token),
        timeout=20,
    )
    if downloaded.status_code == 401:
        raise HTTPException(status_code=401, detail="not authenticated")
    if downloaded.status_code >= 300:
        raise HTTPException(status_code=404, detail="document not found")
    return downloaded.content, row["filename"], row["content_type"]


def documents_ok() -> bool:
    response = httpx.get(
        f"{settings.supabase_url}/rest/v1/documents",
        params={"select": "id", "limit": "1"},
        headers=headers(),
        timeout=5,
    )
    response.raise_for_status()
    return True

import uuid
from datetime import datetime, timezone

import httpx
from fastapi import HTTPException

from app.config import settings


def headers(token: str | None = None) -> dict[str, str]:
    bearer = token or settings.supabase_anon_key
    return {
        "apikey": settings.supabase_anon_key,
        "authorization": f"Bearer {bearer}",
        "content-type": "application/json",
        "accept": "application/json",
    }


def insert_lead(body: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    lead_id = str(uuid.uuid4())
    row = {**body, "id": lead_id, "status": "PENDING", "created_at": now, "updated_at": now}
    response = httpx.post(
        f"{settings.supabase_url}/rest/v1/leads",
        headers={**headers(), "prefer": "return=minimal"},
        json=row,
        timeout=10,
    )
    if response.status_code >= 300:
        raise HTTPException(status_code=502, detail="lead save failed")
    return row


def list_leads(token: str) -> list[dict]:
    response = httpx.get(
        f"{settings.supabase_url}/rest/v1/leads",
        params={"select": "*", "order": "created_at.desc"},
        headers=headers(token),
        timeout=10,
    )
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="not authenticated")
    response.raise_for_status()
    return response.json()


def get_lead(lead_id: str, token: str) -> dict:
    response = httpx.get(
        f"{settings.supabase_url}/rest/v1/leads",
        params={"id": f"eq.{lead_id}", "select": "*"},
        headers=headers(token),
        timeout=10,
    )
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="not authenticated")
    rows = response.json() if response.status_code < 300 else []
    if not rows:
        raise HTTPException(status_code=404, detail="lead not found")
    return rows[0]


def update_status(lead_id: str, token: str) -> dict:
    response = httpx.patch(
        f"{settings.supabase_url}/rest/v1/leads",
        params={"id": f"eq.{lead_id}"},
        headers={**headers(token), "prefer": "return=representation"},
        json={"status": "REACHED_OUT"},
        timeout=10,
    )
    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="not authenticated")
    if response.status_code >= 300:
        code = ""
        try:
            code = response.json().get("code", "")
        except Exception:
            code = ""
        if code == "23514":
            raise HTTPException(status_code=409, detail="lead is already REACHED_OUT")
        raise HTTPException(status_code=502, detail="lead update failed")
    rows = response.json()
    if not rows:
        raise HTTPException(status_code=404, detail="lead not found")
    return rows[0]

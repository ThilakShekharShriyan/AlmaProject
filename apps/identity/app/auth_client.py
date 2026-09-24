import httpx
from fastapi import HTTPException

from app.config import settings


def sign_in(email: str, password: str) -> str:
    response = httpx.post(
        f"{settings.supabase_url}/auth/v1/token",
        params={"grant_type": "password"},
        headers={"apikey": settings.supabase_anon_key, "content-type": "application/json"},
        json={"email": email, "password": password},
        timeout=10,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = response.json().get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return token


def auth_ok() -> bool:
    response = httpx.get(
        f"{settings.supabase_url}/auth/v1/health",
        headers={"apikey": settings.supabase_anon_key},
        timeout=5,
    )
    response.raise_for_status()
    return True

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis

from app.config import settings


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(title="notifications")


def redis_ok() -> bool:
    client = Redis.from_url(settings.redis_url)
    return bool(client.ping())


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        if not redis_ok():
            raise RuntimeError("redis ping failed")
    except Exception as exc:
        raise HTTPException(status_code=503, detail="redis unavailable") from exc
    return HealthResponse(status="ok", service="notifications")

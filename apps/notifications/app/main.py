import logging
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis

from app.config import settings
from app.worker import consume_one

logger = logging.getLogger(__name__)
_stop = threading.Event()


class HealthResponse(BaseModel):
    status: str
    service: str


def redis_ok() -> bool:
    return bool(Redis.from_url(settings.redis_url).ping())


def _loop() -> None:
    while not _stop.is_set():
        try:
            if not consume_one():
                _stop.wait(0.5)
        except Exception:
            logger.exception("notification loop error")
            _stop.wait(1)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _stop.clear()
    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
    yield
    _stop.set()
    thread.join(timeout=2)


app = FastAPI(title="notifications", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        if not redis_ok():
            raise RuntimeError("redis ping failed")
    except Exception as exc:
        raise HTTPException(status_code=503, detail="redis unavailable") from exc
    return HealthResponse(status="ok", service="notifications")

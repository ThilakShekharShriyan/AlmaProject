from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

from app.config import settings

engine = create_engine(settings.documents_database_url, pool_pre_ping=True)


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(title="documents")


def database_ok() -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        database_ok()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return HealthResponse(status="ok", service="documents")

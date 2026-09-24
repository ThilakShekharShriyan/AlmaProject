from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, text

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.models import User
from app.schemas import LoginRequest, TokenResponse
from app.security import create_access_token, hash_password, verify_password


class HealthResponse(BaseModel):
    status: str
    service: str


def database_ok() -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


def seed_attorney() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        existing = session.scalar(select(User).where(User.email == settings.attorney_email))
        if existing is None:
            session.add(
                User(
                    email=settings.attorney_email,
                    password_hash=hash_password(settings.attorney_password),
                )
            )
            session.commit()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    seed_attorney()
    yield


app = FastAPI(title="identity", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        database_ok()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return HealthResponse(status="ok", service="identity")


@app.post("/auth/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.email == body.email))
        if user is None or not verify_password(body.password, user.password_hash):
            raise HTTPException(status_code=401, detail="invalid credentials")
    return TokenResponse(access_token=create_access_token(body.email))

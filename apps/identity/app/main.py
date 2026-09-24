from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.auth_client import auth_ok, sign_in
from app.schemas import LoginRequest, TokenResponse


class HealthResponse(BaseModel):
    status: str
    service: str


def database_ok() -> bool:
    return auth_ok()


app = FastAPI(title="identity")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        database_ok()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return HealthResponse(status="ok", service="identity")


@app.post("/auth/login", response_model=TokenResponse)
def login(body: LoginRequest) -> TokenResponse:
    return TokenResponse(access_token=sign_in(body.email, body.password))

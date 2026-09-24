import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.events import publish_lead_submitted
from app.schemas import LeadCreate, LeadOut, LeadStatus, LeadUpdate
from app.security import bearer, require_token
from app.store import get_lead, insert_lead, list_leads, update_status

logger = logging.getLogger(__name__)


class HealthResponse(BaseModel):
    status: str
    service: str


def database_ok() -> bool:
    return True


app = FastAPI(title="leads")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        database_ok()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return HealthResponse(status="ok", service="leads")


@app.post("/leads", response_model=LeadOut, status_code=201)
def create_lead(body: LeadCreate) -> LeadOut:
    lead = insert_lead(body.model_dump(mode="json"))
    try:
        publish_lead_submitted(lead)
    except Exception:
        logger.exception("lead %s saved but event publish failed", lead["id"])
    return LeadOut.model_validate(lead)


@app.get("/leads", response_model=list[LeadOut])
def list_lead_rows(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> list[LeadOut]:
    token = require_token(credentials)
    return [LeadOut.model_validate(lead) for lead in list_leads(token)]


@app.get("/leads/{lead_id}", response_model=LeadOut)
def get_lead_row(lead_id: str, credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> LeadOut:
    token = require_token(credentials)
    return LeadOut.model_validate(get_lead(lead_id, token))


@app.patch("/leads/{lead_id}", response_model=LeadOut)
def update_lead(
    lead_id: str,
    body: LeadUpdate,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> LeadOut:
    token = require_token(credentials)
    if body.status is not LeadStatus.REACHED_OUT:
        raise HTTPException(status_code=422, detail="status can only move to REACHED_OUT")
    return LeadOut.model_validate(update_status(lead_id, token))

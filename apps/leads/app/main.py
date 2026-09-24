import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import select, text

from app.db import Base, SessionLocal, engine
from app.events import publish_lead_submitted
from app.models import Lead, LeadStatus
from app.schemas import LeadCreate, LeadOut, LeadUpdate
from app.security import bearer, require_attorney

logger = logging.getLogger(__name__)


class HealthResponse(BaseModel):
    status: str
    service: str


def database_ok() -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="leads", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        database_ok()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return HealthResponse(status="ok", service="leads")


@app.post("/leads", response_model=LeadOut, status_code=201)
def create_lead(body: LeadCreate) -> LeadOut:
    with SessionLocal() as session:
        lead = Lead(
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            document_id=body.document_id,
            status=LeadStatus.PENDING,
        )
        session.add(lead)
        session.commit()
        session.refresh(lead)
        try:
            publish_lead_submitted(lead)
        except Exception:
            logger.exception("lead %s saved but event publish failed", lead.id)
        return LeadOut.model_validate(lead)


@app.get("/leads", response_model=list[LeadOut])
def list_leads(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> list[LeadOut]:
    require_attorney(credentials)
    with SessionLocal() as session:
        leads = session.scalars(select(Lead).order_by(Lead.created_at.desc())).all()
        return [LeadOut.model_validate(lead) for lead in leads]


@app.get("/leads/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: str, credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> LeadOut:
    require_attorney(credentials)
    with SessionLocal() as session:
        lead = session.get(Lead, lead_id)
        if lead is None:
            raise HTTPException(status_code=404, detail="lead not found")
        return LeadOut.model_validate(lead)


@app.patch("/leads/{lead_id}", response_model=LeadOut)
def update_lead(
    lead_id: str,
    body: LeadUpdate,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> LeadOut:
    require_attorney(credentials)
    if body.status is not LeadStatus.REACHED_OUT:
        raise HTTPException(status_code=422, detail="status can only move to REACHED_OUT")
    with SessionLocal() as session:
        lead = session.get(Lead, lead_id)
        if lead is None:
            raise HTTPException(status_code=404, detail="lead not found")
        if lead.status is not LeadStatus.PENDING:
            raise HTTPException(status_code=409, detail="lead is already REACHED_OUT")
        lead.status = LeadStatus.REACHED_OUT
        session.commit()
        session.refresh(lead)
        return LeadOut.model_validate(lead)

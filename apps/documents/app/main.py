import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import select, text

from app.config import settings
from app.db import Base, SessionLocal, engine
from app.models import Document
from app.schemas import DocumentCreated
from app.security import bearer, require_attorney

ALLOWED = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class HealthResponse(BaseModel):
    status: str
    service: str


def database_ok() -> bool:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="documents", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    try:
        database_ok()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return HealthResponse(status="ok", service="documents")


@app.post("/documents", response_model=DocumentCreated)
async def upload_document(file: UploadFile = File(...)) -> DocumentCreated:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED:
        raise HTTPException(status_code=422, detail="resume must be pdf, doc, or docx")
    payload = await file.read()
    if len(payload) > settings.max_upload_bytes:
        raise HTTPException(status_code=422, detail="resume exceeds 10 MB")
    if not payload:
        raise HTTPException(status_code=422, detail="resume is empty")
    document_id = str(uuid.uuid4())
    destination = Path(settings.upload_dir) / f"{document_id}{suffix}"
    destination.write_bytes(payload)
    with SessionLocal() as session:
        session.add(
            Document(
                id=document_id,
                filename=file.filename or destination.name,
                content_type=ALLOWED[suffix],
                path=str(destination),
            )
        )
        session.commit()
    return DocumentCreated(document_id=document_id, filename=file.filename or destination.name)


@app.get("/documents/{document_id}")
def download_document(
    document_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> FileResponse:
    require_attorney(credentials)
    with SessionLocal() as session:
        document = session.scalar(select(Document).where(Document.id == document_id))
    if document is None or not Path(document.path).is_file():
        raise HTTPException(status_code=404, detail="document not found")
    return FileResponse(document.path, filename=document.filename, media_type=document.content_type)

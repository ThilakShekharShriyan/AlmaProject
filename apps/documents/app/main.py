import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.schemas import DocumentCreated
from app.security import bearer, require_token
from app.store import documents_ok, fetch_document, save_document
from app.config import settings

ALLOWED = {
    ".pdf": "application/pdf",
    ".doc": "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class HealthResponse(BaseModel):
    status: str
    service: str


def database_ok() -> bool:
    return documents_ok()


app = FastAPI(title="documents")


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
    filename = file.filename or f"{document_id}{suffix}"
    save_document(document_id, filename, ALLOWED[suffix], payload, suffix)
    return DocumentCreated(document_id=document_id, filename=filename)


@app.get("/documents/{document_id}")
def download_document(
    document_id: str,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> Response:
    token = require_token(credentials)
    content, filename, content_type = fetch_document(document_id, token)
    return Response(content, media_type=content_type, headers={"content-disposition": f'attachment; filename="{filename}"'})

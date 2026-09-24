from pydantic import BaseModel


class DocumentCreated(BaseModel):
    document_id: str
    filename: str

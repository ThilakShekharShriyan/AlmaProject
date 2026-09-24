from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class LeadStatus(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"


class LeadCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    document_id: str = Field(min_length=1, max_length=36)


class LeadUpdate(BaseModel):
    status: LeadStatus


class LeadOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    document_id: str
    status: LeadStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

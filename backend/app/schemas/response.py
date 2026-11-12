
from datetime import datetime
from pydantic import BaseModel, Field


class ResponseDraftUpdate(BaseModel):
    draft: str = Field(min_length=1)


class ResponseDraftResponse(BaseModel):
    id: int
    email_id: int
    response_type: str
    draft: str
    confidence: str | None = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DraftGenerationResponse(BaseModel):
    response_required: bool
    response_type: str
    confidence: float
    reason: str
    draft_id: int | None = None
    draft: str = ""
    status: str | None = None
    message: str

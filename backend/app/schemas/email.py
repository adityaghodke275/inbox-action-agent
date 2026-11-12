from datetime import datetime

from pydantic import BaseModel


class EmailCreate(BaseModel):
    sender: str
    recipient: str
    subject: str
    body: str
    received_at: datetime | None = None


class EmailResponse(BaseModel):
    id: int
    sender: str
    recipient: str
    subject: str
    body: str
    received_at: datetime
    is_read: bool
    is_archived: bool
    labels: list[str]
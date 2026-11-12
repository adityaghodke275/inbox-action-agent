from datetime import datetime
from pydantic import BaseModel, Field


class Email(BaseModel):
    id: int
    sender: str
    recipient: str
    subject: str
    body: str
    received_at: datetime
    is_read: bool = False
    is_archived: bool = False
    labels: list[str] = Field(default_factory=list)  
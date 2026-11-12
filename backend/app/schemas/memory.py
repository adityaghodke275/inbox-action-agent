
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    due_date: Optional[datetime] = None
    source_email_id: Optional[int] = None


class TaskStatusUpdate(BaseModel):
    status: Literal["PENDING", "IN_PROGRESS", "COMPLETED", "CANCELLED"]


class ReminderCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    remind_at: datetime
    task_id: Optional[int] = None


class FollowUpCreate(BaseModel):
    subject: str = Field(min_length=1, max_length=255)
    follow_up_date: datetime
    email_id: Optional[int] = None
    description: Optional[str] = None

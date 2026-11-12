from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)

from app.database import Base


class EmailDB(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)

    gmail_id = Column(String, unique=True, nullable=True, index=True)
    thread_id = Column(String, nullable=True, index=True)

    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=True)

    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)

    received_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    is_read = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)

    labels = Column(JSON, nullable=False, default=list)


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    status = Column(String, default="PENDING")
    priority = Column(String, default="MEDIUM")

    due_date = Column(DateTime, nullable=True)

    source_email_id = Column(
        Integer,
        ForeignKey("emails.id"),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )

    completed_at = Column(DateTime, nullable=True)


class ReminderDB(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=True,
    )

    title = Column(String, nullable=False)

    remind_at = Column(DateTime, nullable=False)

    status = Column(String, default="PENDING")

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )


class FollowUpDB(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)

    email_id = Column(
        Integer,
        ForeignKey("emails.id"),
        nullable=True,
    )

    subject = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    follow_up_date = Column(DateTime, nullable=False)

    status = Column(String, default="WAITING")

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )


class AgentActionDB(Base):
    __tablename__ = "agent_actions"

    id = Column(Integer, primary_key=True, index=True)

    email_id = Column(
        Integer,
        ForeignKey("emails.id"),
        nullable=True,
    )

    action_type = Column(String, nullable=False)

    status = Column(String, nullable=False)

    details = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )


class ResponseDraftDB(Base):
    __tablename__ = "response_drafts"

    id = Column(Integer, primary_key=True, index=True)

    email_id = Column(
        Integer,
        ForeignKey("emails.id"),
        nullable=False,
    )

    response_type = Column(String, nullable=False)

    draft = Column(Text, nullable=False)

    confidence = Column(String, nullable=True)

    status = Column(String, default="PENDING_APPROVAL")

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
    )
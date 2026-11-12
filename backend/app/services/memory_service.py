
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.db_models import (
    TaskDB,
    ReminderDB,
    FollowUpDB,
    AgentActionDB,
    ResponseDraftDB,
)


class MemoryService:

    def _get_session(self) -> Session:
        return SessionLocal()

    # -------------------------------
    # ACTION HISTORY
    # -------------------------------

    def log_action(
        self,
        action_type: str,
        status: str,
        email_id: Optional[int] = None,
        details: Optional[str] = None,
    ):
        db = self._get_session()

        try:
            action = AgentActionDB(
                email_id=email_id,
                action_type=action_type,
                status=status,
                details=details,
            )

            db.add(action)
            db.commit()
            db.refresh(action)

            return action.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def get_action_history(self, limit: int = 50):
        db = self._get_session()

        try:
            return (
                db.query(AgentActionDB)
                .order_by(AgentActionDB.created_at.desc())
                .limit(limit)
                .all()
            )
        finally:
            db.close()

    # -------------------------------
    # TASK MANAGEMENT
    # -------------------------------

    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: str = "MEDIUM",
        due_date: Optional[datetime] = None,
        source_email_id: Optional[int] = None,
    ):
        db = self._get_session()

        try:
            task = TaskDB(
                title=title,
                description=description,
                priority=priority.upper(),
                due_date=due_date,
                source_email_id=source_email_id,
                status="PENDING",
            )

            db.add(task)
            db.commit()
            db.refresh(task)

            task_id = task.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        self.log_action(
            action_type="TASK_CREATED",
            status="SUCCESS",
            email_id=source_email_id,
            details=f"Task created: {title}",
        )

        return task_id

    def get_tasks(self, status: Optional[str] = None):
        db = self._get_session()

        try:
            query = db.query(TaskDB)

            if status:
                query = query.filter(
                    TaskDB.status == status.upper()
                )

            return query.order_by(TaskDB.created_at.desc()).all()

        finally:
            db.close()

    def update_task_status(
        self,
        task_id: int,
        status: str,
    ):
        db = self._get_session()

        try:
            task = db.query(TaskDB).filter(
                TaskDB.id == task_id
            ).first()

            if not task:
                return None

            task.status = status.upper()

            if status.upper() == "COMPLETED":
                task.completed_at = datetime.now(timezone.utc)
            else:
                task.completed_at = None

            db.commit()
            db.refresh(task)

            return task

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    # -------------------------------
    # REMINDER MANAGEMENT
    # -------------------------------

    def create_reminder(
        self,
        title: str,
        remind_at: datetime,
        task_id: Optional[int] = None,
    ):
        db = self._get_session()

        try:
            reminder = ReminderDB(
                title=title,
                remind_at=remind_at,
                task_id=task_id,
                status="PENDING",
            )

            db.add(reminder)
            db.commit()
            db.refresh(reminder)

            reminder_id = reminder.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        self.log_action(
            action_type="REMINDER_CREATED",
            status="SUCCESS",
            details=f"Reminder created: {title}",
        )

        return reminder_id

    def get_reminders(self, status: Optional[str] = None):
        db = self._get_session()

        try:
            query = db.query(ReminderDB)

            if status:
                query = query.filter(
                    ReminderDB.status == status.upper()
                )

            return query.order_by(ReminderDB.remind_at.asc()).all()

        finally:
            db.close()

    # -------------------------------
    # FOLLOW-UP MANAGEMENT
    # -------------------------------

    def create_follow_up(
        self,
        subject: str,
        follow_up_date: datetime,
        email_id: Optional[int] = None,
        description: Optional[str] = None,
    ):
        db = self._get_session()

        try:
            follow_up = FollowUpDB(
                email_id=email_id,
                subject=subject,
                description=description,
                follow_up_date=follow_up_date,
                status="WAITING",
            )

            db.add(follow_up)
            db.commit()
            db.refresh(follow_up)

            follow_up_id = follow_up.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        self.log_action(
            action_type="FOLLOW_UP_CREATED",
            status="SUCCESS",
            email_id=email_id,
            details=f"Follow-up created: {subject}",
        )

        return follow_up_id

    def get_follow_ups(self, status: Optional[str] = None):
        db = self._get_session()

        try:
            query = db.query(FollowUpDB)

            if status:
                query = query.filter(
                    FollowUpDB.status == status.upper()
                )

            return query.order_by(
                FollowUpDB.follow_up_date.asc()
            ).all()

        finally:
            db.close()

    
    # -------------------------------
    # RESPONSE DRAFT MANAGEMENT
    # -------------------------------

    def create_response_draft(
        self,
        email_id: int,
        response_type: str,
        draft: str,
        confidence: float | None = None,
    ):
        db = self._get_session()

        try:
            existing = (
                db.query(ResponseDraftDB)
                .filter(
                    ResponseDraftDB.email_id == email_id,
                    ResponseDraftDB.status == "PENDING_APPROVAL",
                )
                .order_by(ResponseDraftDB.created_at.desc())
                .first()
            )

            if existing:
                return {
                    "draft_id": existing.id,
                    "created": False,
                    "message": "A pending draft already exists for this email.",
                }

            response_draft = ResponseDraftDB(
                email_id=email_id,
                response_type=response_type,
                draft=draft,
                confidence=(
                    str(confidence) if confidence is not None else None
                ),
                status="PENDING_APPROVAL",
            )

            db.add(response_draft)
            db.commit()
            db.refresh(response_draft)

            draft_id = response_draft.id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        self.log_action(
            action_type="RESPONSE_DRAFT_CREATED",
            status="SUCCESS",
            email_id=email_id,
            details=f"Response draft created: {response_type}",
        )

        return {
            "draft_id": draft_id,
            "created": True,
            "message": "Response draft saved successfully.",
        }

    def get_response_drafts(self, status=None):
        db = self._get_session()

        try:
            query = db.query(ResponseDraftDB)

            if status:
                query = query.filter(
                    ResponseDraftDB.status == status.upper()
                )

            return query.order_by(
                ResponseDraftDB.created_at.desc()
            ).all()

        finally:
            db.close()

    def get_response_draft(self, draft_id: int):
        db = self._get_session()

        try:
            return (
                db.query(ResponseDraftDB)
                .filter(ResponseDraftDB.id == draft_id)
                .first()
            )

        finally:
            db.close()

    def update_response_draft(self, draft_id: int, draft: str):
        db = self._get_session()

        try:
            response_draft = (
                db.query(ResponseDraftDB)
                .filter(ResponseDraftDB.id == draft_id)
                .first()
            )

            if not response_draft:
                return None

            if response_draft.status != "PENDING_APPROVAL":
                raise ValueError(
                    "Only pending drafts can be edited."
                )

            response_draft.draft = draft

            db.commit()
            db.refresh(response_draft)

            return response_draft

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    def update_draft_status(self, draft_id: int, status: str):
        allowed_statuses = {
            "APPROVED",
            "REJECTED",
        }

        status = status.upper()

        if status not in allowed_statuses:
            raise ValueError("Invalid draft status.")

        db = self._get_session()

        try:
            response_draft = (
                db.query(ResponseDraftDB)
                .filter(ResponseDraftDB.id == draft_id)
                .first()
            )

            if not response_draft:
                return None

            if response_draft.status != "PENDING_APPROVAL":
                raise ValueError(
                    "Only pending drafts can be reviewed."
                )

            response_draft.status = status

            db.commit()
            db.refresh(response_draft)

            email_id = response_draft.email_id

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        self.log_action(
            action_type=f"RESPONSE_DRAFT_{status}",
            status="SUCCESS",
            email_id=email_id,
            details=f"Draft {draft_id} marked {status}.",
        )

        return response_draft

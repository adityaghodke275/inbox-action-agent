
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.db_models import EmailDB
from app.models.email import Email
from app.schemas.email import EmailCreate


class InboxService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self._seed_sample_emails()

    def _seed_sample_emails(self):
        """Insert sample emails only when the database is empty."""

        if self.db.query(EmailDB).first():
            return

        samples = [
            EmailDB(
                id=1,
                sender="hr@techcorp.com",
                recipient="user@example.com",
                subject="Interview Schedule",
                body="Your technical interview has been scheduled for Monday at 10:00 AM.",
                received_at=datetime.now(timezone.utc),
                labels=["work", "interview"],
            ),
            EmailDB(
                id=2,
                sender="newsletter@example.com",
                recipient="user@example.com",
                subject="Weekly Technology Newsletter",
                body="Here are this week's top technology stories and product updates.",
                received_at=datetime.now(timezone.utc),
                labels=["newsletter"],
            ),
            EmailDB(
                id=3,
                sender="client@company.com",
                recipient="user@example.com",
                subject="Project Meeting Request",
                body="Can we schedule a meeting tomorrow to discuss the project requirements?",
                received_at=datetime.now(timezone.utc),
                labels=["work", "important"],
            ),
        ]

        self.db.add_all(samples)
        self.db.commit()

    def _to_email(self, record: EmailDB) -> Email:
        return Email(
            id=record.id,
            sender=record.sender,
            recipient=record.recipient or "",
            subject=record.subject,
            body=record.body,
            received_at=record.received_at,
            is_read=record.is_read,
            is_archived=record.is_archived,
            labels=record.labels or [],
        )

    def get_all_emails(self) -> list[Email]:
        records = (
            self.db.query(EmailDB)
            .order_by(EmailDB.id.asc())
            .all()
        )
        return [self._to_email(record) for record in records]

    def get_email(self, email_id: int) -> Email | None:
        record = self.db.query(EmailDB).filter(
            EmailDB.id == email_id
        ).first()

        if record is None:
            return None

        return self._to_email(record)

    def create_email(self, email_data: EmailCreate) -> Email:
        record = EmailDB(
            sender=email_data.sender,
            recipient=email_data.recipient,
            subject=email_data.subject,
            body=email_data.body,
            received_at=email_data.received_at or datetime.now(timezone.utc),
            labels=[],
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return self._to_email(record)

    def mark_as_read(self, email_id: int) -> Email | None:
        record = self.db.query(EmailDB).filter(
            EmailDB.id == email_id
        ).first()

        if record is None:
            return None

        record.is_read = True
        self.db.commit()
        self.db.refresh(record)

        return self._to_email(record)

    def archive_email(self, email_id: int) -> Email | None:
        record = self.db.query(EmailDB).filter(
            EmailDB.id == email_id
        ).first()

        if record is None:
            return None

        record.is_archived = True
        self.db.commit()
        self.db.refresh(record)

        return self._to_email(record)

    def add_label(self, email_id: int, label: str) -> Email | None:
        record = self.db.query(EmailDB).filter(
            EmailDB.id == email_id
        ).first()

        if record is None:
            return None

        labels = list(record.labels or [])

        if label not in labels:
            labels.append(label)

        record.labels = labels
        self.db.commit()
        self.db.refresh(record)

        return self._to_email(record)

    def close(self):
        self.db.close()

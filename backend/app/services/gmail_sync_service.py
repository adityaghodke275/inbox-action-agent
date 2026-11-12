
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from app.database import SessionLocal
from app.models.db_models import EmailDB
from app.services.gmail_service import GmailService


class GmailSyncService:

    def sync_inbox(self, max_results: int = 20) -> dict:
        gmail = GmailService()
        emails = gmail.get_inbox_messages(max_results=max_results)

        db = SessionLocal()

        imported = 0
        skipped = 0

        try:
            for email_data in emails:
                gmail_id = email_data.get("id")

                if not gmail_id:
                    skipped += 1
                    continue

                existing = (
                    db.query(EmailDB)
                    .filter(EmailDB.gmail_id == gmail_id)
                    .first()
                )

                if existing:
                    skipped += 1
                    continue

                received_at = datetime.now(timezone.utc)

                date_value = email_data.get("date")

                if date_value:
                    try:
                        received_at = parsedate_to_datetime(date_value)

                        if received_at.tzinfo is None:
                            received_at = received_at.replace(
                                tzinfo=timezone.utc
                            )
                    except (TypeError, ValueError, OverflowError):
                        pass

                record = EmailDB(
                    gmail_id=gmail_id,
                    thread_id=email_data.get("thread_id"),
                    sender=email_data.get("sender") or "Unknown sender",
                    recipient=email_data.get("recipient") or None,
                    subject=email_data.get("subject") or "(No subject)",
                    body=email_data.get("body") or "",
                    received_at=received_at,
                    is_read="UNREAD" not in email_data.get("labels", []),
                    is_archived=False,
                    labels=email_data.get("labels", []),
                )

                db.add(record)
                imported += 1

            db.commit()

            return {
                "success": True,
                "total_fetched": len(emails),
                "imported": imported,
                "skipped_duplicates": skipped,
                "message": "Gmail synchronization completed."
            }

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

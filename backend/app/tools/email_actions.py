
from typing import Dict


class EmailActionTool:
    def __init__(self, inbox_service):
        self.inbox_service = inbox_service

    def mark_as_read(self, email_id: int) -> Dict:
        email = self.inbox_service.mark_as_read(email_id)

        return {
            "success": email is not None,
            "action": "mark_as_read",
            "email_id": email_id,
            "message": (
                "Email marked as read"
                if email else "Email not found"
            ),
        }

    def archive(self, email_id: int) -> Dict:
        email = self.inbox_service.archive_email(email_id)

        return {
            "success": email is not None,
            "action": "archive",
            "email_id": email_id,
            "message": (
                "Email archived"
                if email else "Email not found"
            ),
        }

    def add_label(self, email_id: int, label: str) -> Dict:
        email = self.inbox_service.add_label(email_id, label)

        return {
            "success": email is not None,
            "action": "add_label",
            "email_id": email_id,
            "label": label,
            "message": (
                f"Label '{label}' added"
                if email else "Email not found"
            ),
        }

    def delete(self, email_id: int) -> Dict:
        # Soft-delete: preserve the email and mark it archived.
        return self.archive(email_id)

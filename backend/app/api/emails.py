from fastapi import APIRouter, HTTPException

from app.schemas.email import EmailCreate, EmailResponse
from app.services.inbox_service import InboxService
from app.agents.inbox_agent import analyze_email, execute_email_action
from app.services.gmail_sync_service import GmailSyncService


router = APIRouter(
    prefix="/emails",
    tags=["Emails"],
)

inbox_service = InboxService()


@router.get("/", response_model=list[EmailResponse])
def get_emails():
    return inbox_service.get_all_emails()


@router.get("/{email_id}", response_model=EmailResponse)
def get_email(email_id: int):
    email = inbox_service.get_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    return email

@router.get("/{email_id}/analyze")
def analyze_email_endpoint(email_id: int):
    email = inbox_service.get_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    return analyze_email(email)

@router.post("/{email_id}/execute")
def execute_email_action_endpoint(email_id: int):
    email = inbox_service.get_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )

    return execute_email_action(
        email=email,
        inbox_service=inbox_service,
    )


@router.post("/", response_model=EmailResponse)
def create_email(email_data: EmailCreate):
    return inbox_service.create_email(email_data)


@router.patch("/{email_id}/read", response_model=EmailResponse)
def mark_email_as_read(email_id: int):
    email = inbox_service.mark_as_read(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found",
        )


@router.post("/sync-gmail")
def sync_gmail_inbox(max_results: int = 20):
    try:
        sync_service = GmailSyncService()
        return sync_service.sync_inbox(max_results=max_results)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Gmail synchronization failed: {str(error)}"
        )

    return email
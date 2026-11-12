
from fastapi import APIRouter, HTTPException, Query

from app.agents.response_agent import ResponseIntelligenceAgent
from app.services.inbox_service import InboxService
from app.services.memory_service import MemoryService
from app.schemas.response import (
    ResponseDraftUpdate,
    ResponseDraftResponse,
    DraftGenerationResponse,
)

router = APIRouter(
    prefix="/responses",
    tags=["Response Intelligence"],
)

inbox_service = InboxService()
memory_service = MemoryService()
response_agent = ResponseIntelligenceAgent()


@router.post(
    "/emails/{email_id}/generate",
    response_model=DraftGenerationResponse,
)
def generate_response_draft(email_id: int):

    email = inbox_service.get_email(email_id)

    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found.",
        )

    try:
        result = response_agent.analyze_email(
            sender=email.sender,
            subject=email.subject,
            body=email.body,
        )

        if not result["response_required"]:
            memory_service.log_action(
                action_type="RESPONSE_NOT_REQUIRED",
                status="SUCCESS",
                email_id=email_id,
                details=result["reason"],
            )

            return {
                **result,
                "draft_id": None,
                "status": None,
                "message": "No reply is required for this email.",
            }

        saved = memory_service.create_response_draft(
            email_id=email_id,
            response_type=result["response_type"],
            draft=result["draft"],
            confidence=result["confidence"],
        )

        return {
            **result,
            "draft_id": saved["draft_id"],
            "status": "PENDING_APPROVAL",
            "message": saved["message"],
        }

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Draft generation failed: {str(error)}",
        )


@router.get(
    "/drafts",
    response_model=list[ResponseDraftResponse],
)
def get_response_drafts(
    status: str | None = Query(default=None),
):
    return memory_service.get_response_drafts(status=status)


@router.get(
    "/drafts/{draft_id}",
    response_model=ResponseDraftResponse,
)
def get_response_draft(draft_id: int):

    draft = memory_service.get_response_draft(draft_id)

    if draft is None:
        raise HTTPException(
            status_code=404,
            detail="Response draft not found.",
        )

    return draft


@router.patch(
    "/drafts/{draft_id}",
    response_model=ResponseDraftResponse,
)
def edit_response_draft(
    draft_id: int,
    payload: ResponseDraftUpdate,
):

    try:
        draft = memory_service.update_response_draft(
            draft_id=draft_id,
            draft=payload.draft,
        )

        if draft is None:
            raise HTTPException(
                status_code=404,
                detail="Response draft not found.",
            )

        return draft

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


@router.post("/drafts/{draft_id}/approve")
def approve_response_draft(draft_id: int):

    try:
        draft = memory_service.update_draft_status(
            draft_id=draft_id,
            status="APPROVED",
        )

        if draft is None:
            raise HTTPException(
                status_code=404,
                detail="Response draft not found.",
            )

        return {
            "success": True,
            "draft_id": draft.id,
            "status": draft.status,
            "message": (
                "Draft approved. No email has been sent."
            ),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


@router.post("/drafts/{draft_id}/reject")
def reject_response_draft(draft_id: int):

    try:
        draft = memory_service.update_draft_status(
            draft_id=draft_id,
            status="REJECTED",
        )

        if draft is None:
            raise HTTPException(
                status_code=404,
                detail="Response draft not found.",
            )

        return {
            "success": True,
            "draft_id": draft.id,
            "status": draft.status,
            "message": "Response draft rejected.",
        }

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )

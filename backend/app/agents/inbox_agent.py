from app.agents.classifier import classify_email
from app.agents.summarizer import summarize_email
from app.tools.email_actions import EmailActionTool



def analyze_email(email) -> dict:
    """
    Analyze an email and determine the recommended action.
    """

    classification = classify_email(
        subject=email.subject,
        body=email.body,
    )

    summary_result = summarize_email(
        subject=email.subject,
        body=email.body,
    )

    summary = summary_result["summary"]
    category = classification["category"]
    priority = classification["priority"]

    # SECURITY: Never automatically archive security alerts.
    if category == "security_alert":
        action = "review"

    elif category == "important":
        action = "review"

    elif category in ["newsletter", "promotional"]:
        action = "archive"

    else:
        action = "keep"

    return {
        "email_id": email.id,
        "category": category,
        "priority": priority,
        "summary": summary,
        "recommended_action": action,
    }



def execute_email_action(email, inbox_service) -> dict:
    """
    Analyze an email and execute the recommended action.
    """

    analysis = analyze_email(email)

    action_tool = EmailActionTool(inbox_service)

    action = analysis["recommended_action"]

    if analysis["category"] == "security_alert":
        action = "review"

    if action == "archive":

        result = action_tool.archive(email.id)

    elif action == "review":

        result = {
            "success": True,
            "action": "review",
            "email_id": email.id,
            "message": "Email requires human review",
            "requires_approval": True,
        }

    elif action == "keep":

        result = {
            "success": True,
            "action": "keep",
            "email_id": email.id,
            "message": "Email kept in inbox",
        }

    else:

        result = {
            "success": False,
            "action": action,
            "email_id": email.id,
            "message": "Unknown action",
        }

    return {
        "analysis": analysis,
        "execution": result,
    }
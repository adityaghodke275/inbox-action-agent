
from typing import Dict


def classify_email(subject: str, body: str) -> Dict[str, str]:
    """
    Classify emails by category and priority.

    Categories:
        security_alert
        important
        newsletter
        promotional
        account_notification
        general
    """

    subject_text = (subject or "").lower().strip()
    body_text = (body or "").lower().strip()
    text = f"{subject_text} {body_text}"

    # 1. SECURITY ALERTS
    security_keywords = [
        "security alert",
        "new sign-in",
        "new signin",
        "suspicious sign-in",
        "suspicious activity",
        "unrecognized device",
        "unknown device",
        "password changed",
        "password reset",
        "recovery code",
        "account compromised",
        "unauthorized access",
        "unusual login",
        "2-step verification",
    ]

    if any(keyword in text for keyword in security_keywords):
        return {
            "category": "security_alert",
            "priority": "critical",
        }

    # 2. HIGH-PRIORITY WORK EMAILS
    important_keywords = [
        "interview",
        "meeting invitation",
        "meeting scheduled",
        "appointment",
        "deadline",
        "urgent",
        "action required",
        "submission due",
        "project review",
        "important",
    ]

    if any(keyword in text for keyword in important_keywords):
        return {
            "category": "important",
            "priority": "high",
        }

    # 3. NEWSLETTERS
    newsletter_keywords = [
        "newsletter",
        "weekly update",
        "product updates",
        "technology stories",
        "monthly digest",
        "weekly digest",
    ]

    if any(keyword in text for keyword in newsletter_keywords):
        return {
            "category": "newsletter",
            "priority": "low",
        }

    # 4. PROMOTIONAL EMAILS
    promotional_keywords = [
        "special offer",
        "limited time offer",
        "discount",
        "sale",
        "coupon",
        "shop now",
        "exclusive deal",
        "promotional offer",
    ]

    if any(keyword in text for keyword in promotional_keywords):
        return {
            "category": "promotional",
            "priority": "low",
        }

    # 5. ACCOUNT NOTIFICATIONS
    account_keywords = [
        "account notification",
        "account activity",
        "device setup",
        "finish setting up",
        "subscription renewed",
        "payment received",
        "verification successful",
    ]

    if any(keyword in text for keyword in account_keywords):
        return {
            "category": "account_notification",
            "priority": "medium",
        }

    # 6. GENERAL EMAIL
    return {
        "category": "general",
        "priority": "medium",
    }

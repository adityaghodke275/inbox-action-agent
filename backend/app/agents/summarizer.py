from typing import Dict


def summarize_email(subject: str, body: str) -> Dict[str, str]:
    """
    Generate a concise summary of an email.

    Args:
        subject: Email subject.
        body: Email body.

    Returns:
        Dictionary containing the email summary.
    """

    text = body.strip()

    if not text:
        return {
            "summary": "No email content available."
        }

    # Basic first implementation.
    # We will replace this with the LLM-based summarizer next.
    sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]

    if len(sentences) > 2:
        summary = ". ".join(sentences[:2]) + "."
    else:
        summary = text

    return {
        "summary": summary
    }
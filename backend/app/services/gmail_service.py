import os
import base64
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Gmail permission for the first stage.
# Read-only means the agent cannot modify or send emails yet.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


class GmailService:
    """
    Gmail API service for Inbox Action Agent.

    Current stage:
    - Authenticate with Google
    - Read Gmail messages
    - Extract basic email information

    No email modification or sending is allowed yet.
    """

    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        """
        Authenticate the Gmail account using OAuth 2.0.
        """

        creds: Optional[Credentials] = None

        # Reuse previously generated OAuth token.
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES
            )

        # Refresh expired credentials when possible.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # First-time authentication.
        elif not creds or not creds.valid:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"credentials.json not found at: {CREDENTIALS_FILE}"
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(
                host="localhost",
                port=0,
                open_browser=False
            )

            # Save token for future requests.
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return build(
            "gmail",
            "v1",
            credentials=creds
        )

    def get_profile(self) -> Dict:
        """
        Get the authenticated Gmail account information.
        """

        profile = (
            self.service.users()
            .getProfile(userId="me")
            .execute()
        )

        return profile

    def list_messages(
        self,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Retrieve messages from the Gmail inbox.
        """

        response = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                labelIds=["INBOX"],
                maxResults=max_results
            )
            .execute()
        )

        messages = response.get("messages", [])

        return messages

    def get_message(
        self,
        message_id: str
    ) -> Dict:
        """
        Retrieve a complete Gmail message.
        """

        return (
            self.service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full"
            )
            .execute()
        )

    def get_inbox_messages(
        self,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Retrieve and parse inbox messages into a simpler structure.
        """

        messages = self.list_messages(max_results)

        emails = []

        for message in messages:
            full_message = self.get_message(
                message["id"]
            )

            emails.append(
                self._parse_message(full_message)
            )

        return emails

    def _parse_message(
        self,
        message: Dict
    ) -> Dict:
        """
        Convert Gmail API message format into
        a simple email structure.
        """

        payload = message.get("payload", {})
        headers = payload.get("headers", [])

        subject = ""
        sender = ""
        recipient = ""
        date = ""

        for header in headers:
            name = header.get("name", "").lower()
            value = header.get("value", "")

            if name == "subject":
                subject = value

            elif name == "from":
                sender = value

            elif name == "to":
                recipient = value

            elif name == "date":
                date = value

        body = self._extract_body(payload)

        return {
            "id": message.get("id"),
            "thread_id": message.get("threadId"),
            "sender": sender,
            "recipient": recipient,
            "subject": subject,
            "date": date,
            "body": body,
            "snippet": message.get("snippet", ""),
            "labels": message.get("labelIds", []),
        }

    def _extract_body(self, payload: Dict) -> str:
        """
        Extract plain-text email body from a Gmail message.
        """

        body = payload.get("body", {})
        data = body.get("data")

        if data:
            return self._decode_body(data)

        parts = payload.get("parts", [])

        for part in parts:
            mime_type = part.get("mimeType", "")

            if mime_type == "text/plain":
                data = part.get("body", {}).get("data")

                if data:
                    return self._decode_body(data)

        # Handle nested multipart messages.
        for part in parts:
            if "parts" in part:
                nested_body = self._extract_body(part)

                if nested_body:
                    return nested_body

        return ""

    @staticmethod
    def _decode_body(data: str) -> str:
        """
        Decode Gmail's URL-safe Base64 email body.
        """

        try:
            decoded = base64.urlsafe_b64decode(
                data.encode("UTF-8")
            )

            return decoded.decode(
                "UTF-8",
                errors="replace"
            )

        except Exception:
            return ""
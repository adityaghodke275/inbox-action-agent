from app.services.gmail_service import GmailService


def main():
    print("=" * 60)
    print("Inbox Action Agent - Gmail OAuth Test")
    print("=" * 60)

    print("\nConnecting to Gmail...")

    gmail = GmailService()

    print("✅ Gmail authentication successful!")

    profile = gmail.get_profile()

    print("\nAuthenticated Gmail account:")
    print(f"Email: {profile.get('emailAddress')}")
    print(f"Messages total: {profile.get('messagesTotal')}")
    print(f"Threads total: {profile.get('threadsTotal')}")

    print("\nFetching inbox messages...")

    emails = gmail.get_inbox_messages(max_results=5)

    print(f"Found {len(emails)} inbox messages.\n")

    for index, email in enumerate(emails, start=1):
        print("-" * 60)
        print(f"Email #{index}")
        print(f"ID: {email['id']}")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print(f"Snippet: {email['snippet']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
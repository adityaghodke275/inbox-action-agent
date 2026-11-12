
from app.agents.response_agent import ResponseIntelligenceAgent


def main():
    agent = ResponseIntelligenceAgent()

    test_cases = [
        {
            "name": "THANK YOU DETECTION",
            "sender": "mentor@example.com",
            "subject": "Project Reference Material",
            "body": """
            Hello,

            I have attached the reference material you requested
            for your AI project. I hope it helps you with your work.

            Best regards,
            Mentor
            """,
            "expected": "THANK"
        },
        {
            "name": "ACKNOWLEDGEMENT",
            "sender": "team@example.com",
            "subject": "Project Meeting Update",
            "body": """
            Hello,

            The project review meeting has been moved to
            Friday at 3 PM. Please take note of the updated schedule.

            Please acknowledge receipt of this updated schedule
            so that we know you have received the information.



            Regards,
            Team
            """,
            "expected": "ACKNOWLEDGE"
        },
        {
            "name": "NO REPLY REQUIRED",
            "sender": "newsletter@example.com",
            "subject": "Weekly Technology Newsletter",
            "body": """
            Here are this week's technology updates,
            product announcements and industry news.

            Read our latest articles on our website.
            """,
            "expected": "NO_REPLY"
        }
    ]

    for test in test_cases:
        print("\n" + "=" * 60)
        print("TEST:", test["name"])
        print("=" * 60)

        try:
            result = agent.analyze_email(
                sender=test["sender"],
                subject=test["subject"],
                body=test["body"]
            )

            print("Expected Type:", test["expected"])
            print("Actual Type:", result["response_type"])
            print("Response Required:", result["response_required"])
            print("Confidence:", result["confidence"])
            print("Reason:", result["reason"])
            print("Draft:", result["draft"] or "No draft generated")

            if result["response_type"] == test["expected"]:
                print("RESULT: PASS")
            else:
                print("RESULT: REVIEW")

        except Exception as error:
            print("RESULT: ERROR")
            print("Error:", str(error))


if __name__ == "__main__":
    main()

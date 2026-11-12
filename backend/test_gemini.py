from app.services.gemini_service import GeminiService


def main():
    gemini = GeminiService()

    response = gemini.generate_text(
        "Reply with exactly: Inbox Action Agent Gemini connection successful."
    )

    print("\n===== GEMINI CONNECTION TEST =====")
    print(response)


if __name__ == "__main__":
    main()
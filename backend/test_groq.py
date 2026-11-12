
from app.services.llm_service import LLMService


def main():
    llm = LLMService()

    response = llm.generate_text(
        "Reply with exactly: "
        "Inbox Action Agent Groq connection successful."
    )

    print("\n===== GROQ CONNECTION TEST =====")
    print(response)


if __name__ == "__main__":
    main()

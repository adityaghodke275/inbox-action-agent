
from datetime import datetime, timedelta, timezone

from app.services.memory_service import MemoryService


def main():
    memory = MemoryService()

    print("\n===== MEMORY SERVICE TEST =====")

    # 1. Create a task
    task_id = memory.create_task(
        title="Submit project report",
        description="Complete and submit the project report.",
        priority="HIGH",
        due_date=datetime.now(timezone.utc) + timedelta(days=3),
    )

    print(f"\nTask created: {task_id}")

    # 2. Create a reminder
    reminder_id = memory.create_reminder(
        title="Reminder: Submit project report",
        remind_at=datetime.now(timezone.utc) + timedelta(days=2),
        task_id=task_id,
    )

    print(f"Reminder created: {reminder_id}")

    # 3. Create a follow-up
    follow_up_id = memory.create_follow_up(
        subject="Internship application follow-up",
        description="Check for an update from the company.",
        follow_up_date=datetime.now(timezone.utc) + timedelta(days=5),
    )

    print(f"Follow-up created: {follow_up_id}")

    # 4. Retrieve tasks
    print("\n===== SAVED TASKS =====")

    for task in memory.get_tasks():
        print(task.id, task.title, task.status, task.priority)

    # 5. Retrieve reminders
    print("\n===== SAVED REMINDERS =====")

    for reminder in memory.get_reminders():
        print(reminder.id, reminder.title, reminder.status)

    # 6. Retrieve follow-ups
    print("\n===== SAVED FOLLOW-UPS =====")

    for follow_up in memory.get_follow_ups():
        print(follow_up.id, follow_up.subject, follow_up.status)

    # 7. Retrieve action history
    print("\n===== ACTION HISTORY =====")

    for action in memory.get_action_history(limit=10):
        print(action.id, action.action_type, action.status)

    print("\n===== TEST COMPLETED =====")


if __name__ == "__main__":
    main()

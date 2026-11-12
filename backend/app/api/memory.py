
from fastapi import APIRouter, HTTPException, Query

from app.schemas.memory import (
    TaskCreate,
    TaskStatusUpdate,
    ReminderCreate,
    FollowUpCreate,
)
from app.services.memory_service import MemoryService


router = APIRouter(tags=["Agent Memory"])


def serialize_task(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "source_email_id": task.source_email_id,
        "created_at": task.created_at,
        "completed_at": task.completed_at,
    }


def serialize_reminder(reminder):
    return {
        "id": reminder.id,
        "title": reminder.title,
        "remind_at": reminder.remind_at,
        "task_id": reminder.task_id,
        "status": reminder.status,
        "created_at": reminder.created_at,
    }


def serialize_follow_up(item):
    return {
        "id": item.id,
        "subject": item.subject,
        "description": item.description,
        "follow_up_date": item.follow_up_date,
        "email_id": item.email_id,
        "status": item.status,
        "created_at": item.created_at,
    }


def serialize_action(action):
    return {
        "id": action.id,
        "email_id": action.email_id,
        "action_type": action.action_type,
        "status": action.status,
        "details": action.details,
        "created_at": action.created_at,
    }


# -------------------------------
# TASKS
# -------------------------------

@router.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    memory = MemoryService()

    task_id = memory.create_task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_date=payload.due_date,
        source_email_id=payload.source_email_id,
    )

    tasks = memory.get_tasks()
    task = next((item for item in tasks if item.id == task_id), None)

    if task is None:
        raise HTTPException(status_code=500, detail="Task was created but could not be retrieved")

    return serialize_task(task)


@router.get("/tasks")
def get_tasks(
    status: str | None = Query(default=None)
):
    memory = MemoryService()
    return [
        serialize_task(task)
        for task in memory.get_tasks(status=status)
    ]


@router.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    payload: TaskStatusUpdate,
):
    memory = MemoryService()

    task = memory.update_task_status(
        task_id=task_id,
        status=payload.status,
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return serialize_task(task)


# -------------------------------
# REMINDERS
# -------------------------------

@router.post("/reminders", status_code=201)
def create_reminder(payload: ReminderCreate):
    memory = MemoryService()

    reminder_id = memory.create_reminder(
        title=payload.title,
        remind_at=payload.remind_at,
        task_id=payload.task_id,
    )

    reminders = memory.get_reminders()
    reminder = next(
        (item for item in reminders if item.id == reminder_id),
        None,
    )

    if reminder is None:
        raise HTTPException(status_code=500, detail="Reminder could not be retrieved")

    return serialize_reminder(reminder)


@router.get("/reminders")
def get_reminders(
    status: str | None = Query(default=None)
):
    memory = MemoryService()

    return [
        serialize_reminder(item)
        for item in memory.get_reminders(status=status)
    ]


# -------------------------------
# FOLLOW-UPS
# -------------------------------

@router.post("/follow-ups", status_code=201)
def create_follow_up(payload: FollowUpCreate):
    memory = MemoryService()

    follow_up_id = memory.create_follow_up(
        subject=payload.subject,
        description=payload.description,
        follow_up_date=payload.follow_up_date,
        email_id=payload.email_id,
    )

    items = memory.get_follow_ups()
    item = next(
        (entry for entry in items if entry.id == follow_up_id),
        None,
    )

    if item is None:
        raise HTTPException(status_code=500, detail="Follow-up could not be retrieved")

    return serialize_follow_up(item)


@router.get("/follow-ups")
def get_follow_ups(
    status: str | None = Query(default=None)
):
    memory = MemoryService()

    return [
        serialize_follow_up(item)
        for item in memory.get_follow_ups(status=status)
    ]


# -------------------------------
# AGENT ACTION HISTORY
# -------------------------------

@router.get("/history")
def get_action_history(
    limit: int = Query(default=50, ge=1, le=200)
):
    memory = MemoryService()

    return [
        serialize_action(action)
        for action in memory.get_action_history(limit=limit)
    ]

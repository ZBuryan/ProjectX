from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..services.task_service import TaskService
from ..services.user_service import UserService
from ..dto import task_dto
from ..database.models.task import TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=task_dto.TaskResponse, summary="Create a new task")
def create_task(
    task: task_dto.TaskCreate, creator_id: int, db: Session = Depends(get_db)
):
    """
    Create a new task. Creator ID is required.
    """
    creator = UserService.get_user(db, user_id=creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")
    return TaskService.create_task(db=db, task=task, creator_id=creator_id)


@router.get("/", response_model=List[task_dto.TaskResponse], summary="Get all tasks")
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get list of all tasks with pagination.
    """
    tasks = TaskService.get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.get(
    "/{task_id}", response_model=task_dto.TaskResponse, summary="Get task by ID"
)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by its ID.
    """
    task = TaskService.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post(
    "/{task_id}/assign",
    response_model=task_dto.TaskResponse,
    summary="Assign task to user",
)
def assign_task(
    task_id: int, assignment: task_dto.TaskAssign, db: Session = Depends(get_db)
):
    """
    Assign a task to a user who will complete it. Task must be in NEW status.
    """
    assignee = UserService.get_user(db, user_id=assignment.assignee_id)
    if assignee is None:
        raise HTTPException(status_code=404, detail="Assignee not found")

    task = TaskService.assign_task(
        db, task_id=task_id, assignee_id=assignment.assignee_id
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != TaskStatus.NEW:
        raise HTTPException(
            status_code=400, detail="Can only assign tasks with NEW status"
        )
    return task


@router.put(
    "/{task_id}/status",
    response_model=task_dto.TaskResponse,
    summary="Update task status",
)
def update_task_status(
    task_id: int,
    status_update: task_dto.TaskUpdateStatus,
    db: Session = Depends(get_db),
):
    """
    Update task status. Available statuses: NEW, DONE, EXPIRED.
    Note: Setting to DONE will check if task is not expired.
    """
    task = TaskService.update_task_status(
        db, task_id=task_id, status=status_update.status
    )
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post(
    "/check-expired",
    response_model=List[task_dto.TaskResponse],
    summary="Check for expired tasks",
)
def check_expired_tasks(db: Session = Depends(get_db)):
    """
    Check and mark expired tasks. Tasks past their due_date will be marked as EXPIRED.
    """
    return TaskService.check_expired_tasks(db)

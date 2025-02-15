from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..database.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str
    points: int
    due_date: datetime


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    points: int
    status: TaskStatus
    created_at: datetime
    due_date: datetime
    completed_at: Optional[datetime] = None
    creator_id: int
    assignee_id: Optional[int] = None

    class Config:
        from_attributes = True


class TaskUpdateStatus(BaseModel):
    status: TaskStatus


class TaskAssign(BaseModel):
    assignee_id: int


class TaskTemplate(BaseModel):
    title: str
    description: str
    points: int

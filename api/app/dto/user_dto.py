from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from .task_dto import TaskResponse


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..connection import Base


class TaskStatus(str, enum.Enum):
    NEW = "NEW"
    EXPIRED = "EXPIRED"
    DONE = "DONE"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    points = Column(Integer)
    status = Column(Enum(TaskStatus), default=TaskStatus.NEW)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    creator = relationship("User", foreign_keys=[creator_id], backref="created_tasks")
    assignee = relationship(
        "User", foreign_keys=[assignee_id], backref="assigned_tasks"
    )

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List
from ..database.models.task import Task, TaskStatus
from ..database.models.user import User
from ..dto import task_dto, stats_dto


class TaskService:
    @staticmethod
    def get_task(db: Session, task_id: int):
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_tasks(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Task).offset(skip).limit(limit).all()

    @staticmethod
    def create_task(db: Session, task: task_dto.TaskCreate, creator_id: int):
        db_task = Task(
            title=task.title,
            description=task.description,
            points=task.points,
            due_date=task.due_date,
            status=TaskStatus.NEW,
            creator_id=creator_id,
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def assign_task(db: Session, task_id: int, assignee_id: int):
        task = db.query(Task).filter(Task.id == task_id).first()
        if task and task.status == TaskStatus.NEW:
            task.assignee_id = assignee_id
            db.commit()
            db.refresh(task)
        return task

    @staticmethod
    def update_task_status(db: Session, task_id: int, status: TaskStatus):
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            # Sprawdzanie czy task może zmienić status
            if status == TaskStatus.DONE:
                if datetime.utcnow() > task.due_date:
                    task.status = TaskStatus.EXPIRED
                else:
                    task.status = status
                    task.completed_at = datetime.utcnow()
            else:
                task.status = status
            db.commit()
            db.refresh(task)
        return task

    @staticmethod
    def check_expired_tasks(db: Session):
        current_time = datetime.utcnow()
        tasks = (
            db.query(Task)
            .filter(Task.status == TaskStatus.NEW)
            .filter(Task.due_date < current_time)
            .all()
        )
        for task in tasks:
            task.status = TaskStatus.EXPIRED
        db.commit()
        return tasks

    @staticmethod
    def get_user_monthly_stats(db: Session) -> List[stats_dto.UserStatsResponse]:
        current_month = datetime.utcnow().month
        stats = (
            db.query(
                User.id,
                User.username,
                func.coalesce(func.sum(Task.points), 0).label("total_points"),
                func.coalesce(func.count(Task.id), 0).label("completed_tasks"),
            )
            .outerjoin(
                Task,
                (User.id == Task.assignee_id)
                & (Task.status == TaskStatus.DONE)
                & (func.extract("month", Task.completed_at) == current_month),
            )
            .group_by(User.id, User.username)
            .order_by(func.coalesce(func.sum(Task.points), 0).desc())
            .all()
        )

        return [
            stats_dto.UserStatsResponse(
                user_id=user_id,
                username=username,
                total_points=total_points,
                completed_tasks=completed_tasks,
            )
            for user_id, username, total_points, completed_tasks in stats
        ]

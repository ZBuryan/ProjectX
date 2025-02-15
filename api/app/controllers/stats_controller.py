from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..services.task_service import TaskService
from ..dto import stats_dto

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.get("/monthly", response_model=List[stats_dto.UserStatsResponse])
def get_monthly_stats(db: Session = Depends(get_db)):
    return TaskService.get_user_monthly_stats(db)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.connection import get_db
from ..services.user_service import UserService
from ..dto import user_dto

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=user_dto.UserResponse)
def create_user(user: user_dto.UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, user=user)


@router.get("/", response_model=List[user_dto.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user_dto.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

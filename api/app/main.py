from fastapi import FastAPI
from .database.connection import engine, Base
from .database.models.user import User
from .database.models.task import Task
from .controllers import user_controller, task_controller, stats_controller

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Household Tasks Manager")

# Include routers
app.include_router(user_controller.router)
app.include_router(task_controller.router)
app.include_router(stats_controller.router)

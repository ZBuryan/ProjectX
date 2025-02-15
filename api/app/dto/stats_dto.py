from pydantic import BaseModel


class UserStatsResponse(BaseModel):
    user_id: int
    username: str
    total_points: int
    completed_tasks: int

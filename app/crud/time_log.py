from pydantic import BaseModel
from datetime import date
from app.models.user import UserResponse
from task import TaskModel


class TimeLogModel(BaseModel):
    id: int
    user_id: int
    task_id: int
    minutes: int
    logged_at: date
    user: UserResponse
    task: TaskModel

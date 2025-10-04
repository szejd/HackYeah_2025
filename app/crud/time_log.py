from pydantic import BaseModel
from datetime import date
from user import UserModel
from task import TaskModel

class TimeLogModel(BaseModel):
    id: int
    user_id: int
    task_id: int
    minutes: int
    logged_at: date
    user: UserModel
    task: TaskModel
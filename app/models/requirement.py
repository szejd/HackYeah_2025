from pydantic import BaseModel
from task import TaskModel
from skill import SkillModel

class RequirementModel(BaseModel):
    id: int
    description: str
    task_id: int
    skill_id: int
    task: TaskModel
    skill: SkillModel
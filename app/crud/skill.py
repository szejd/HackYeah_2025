from pydantic import BaseModel
from volunteer import VolunteerModel
from requirement import RequirementModel


class SkillModel(BaseModel):
    id: int
    skill_name: str
    volunteers: list[VolunteerModel]
    requirements: list[RequirementModel]

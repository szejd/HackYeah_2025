from pydantic import BaseModel
from time_log import TimeLogModel
from event import EventModel
from organisation import OrganisationModel
from requirement import RequirementModel

class TaskModel(BaseModel):
    id: int
    name: str
    description: str
    estimation_minutes: int
    organisation_id: int
    event_id: int | None = None
    event: EventModel | None = None
    organisation: OrganisationModel = None
    time_logs: list[TimeLogModel]
    requirements: list[RequirementModel]

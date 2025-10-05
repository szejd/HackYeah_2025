from datetime import date

from pydantic import BaseModel
from event import EventModel
from app.models.user import UserResponse


class RegistrationModel(BaseModel):
    id: int
    user_id: int
    event_id: int
    registered_at: date
    status: str
    user: UserResponse
    event: EventModel

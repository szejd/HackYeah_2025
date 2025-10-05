from pydantic import BaseModel
from user import UserModel
from event import EventModel
from datetime import date


class RegistrationModel(BaseModel):
    id: int
    user_id: int
    event_id: int
    registered_at: date
    status: str
    user: UserModel
    event: EventModel

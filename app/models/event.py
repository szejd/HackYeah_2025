from pydantic import BaseModel
from datetime import date

from location import Location
from organisation import OrganisationModel
from task import TaskModel
from registration import RegistrationModel
from certificate import CertificateModel
from app.schemas.enums import RegistrationStatus


class EventModel(BaseModel):
    id: int
    name: str
    description: str
    start_date: date
    end_date: date
    signup_start: date
    signup_end: date
    location_id: int
    organisation_id: int
    location: Location
    organisation: OrganisationModel
    task: TaskModel
    registrations: list[RegistrationModel]
    certificates: list[CertificateModel]


class EventUserRegistration(BaseModel):
    user_id: int
    event_id: int
    status: RegistrationStatus = RegistrationStatus.PENDING


class EventCreation(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    signup_start: date
    signup_end: date
    address: str
    organisation: OrganisationModel

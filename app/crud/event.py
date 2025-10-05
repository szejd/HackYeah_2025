from app.schemas.db_models import Registration
from app.models.event import EventUserRegistration
from sqlalchemy.orm import Session



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

def register_for_event(session: Session, registration_data: EventUserRegistration) -> Registration:
    registration = Registration(
        user_id=registration_data.user_id, event_id=registration_data.event_id, status=registration_data.status
    )
    try:
        session.add(registration)
        session.commit()
        session.refresh(registration)
    except Exception as e:
        session.rollback()
        raise e
    return registration

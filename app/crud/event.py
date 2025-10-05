from app.schemas.db_models import Registration
from app.models.event import EventUserRegistration
from sqlalchemy.orm import Session


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


def create_event(session: Session):
    pass

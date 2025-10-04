from pydantic import BaseModel
from datetime import date
from app.schemas.db_models import User, Volunteer, Organisation, Coordinator
from app.schemas.enums import UserType

class UserInfo(BaseModel):
    email: str
    password_hash: str
    user_type: UserType
    created_at: date | None = None
    updated_at: date | None = None

class VolunteerInfo(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    phone_number: str

class OrganisationInfo(BaseModel):
    org_name: str
    contact_person: str
    description: str
    phone_number: str
    address: str
    verified: bool = False

class CoordinatorInfo(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    school: str
    verified: bool = False


def add_user(session, user: UserInfo, other_info: BaseModel) -> User | None:
    """
    Adds new user to db.

    :param session: SQLAlchemy Session
    :param user: data for User
    :param other_info: data specific for Volunteer/Organisation/Coordinator
    :return: User or None if not added
    """
    if (
            (user.user_type == UserType.VOLUNTEER and not isinstance(other_info, VolunteerInfo)) or
            (user.user_type == UserType.ORGANISATION and not isinstance(other_info, OrganisationInfo)) or
            (user.user_type == UserType.COORDINATOR and not isinstance(other_info, CoordinatorInfo))
    ):
        raise TypeError("Brak obowiązkowych informacji dla podanego typu użytkownika!")

    new_user = User(
        email=user.email,
        password_hash=user.password_hash,
        user_type=user.user_type
    )
    try:
        session.add(new_user)
        session.flush()
        if user.user_type == UserType.VOLUNTEER:
            volunteer = Volunteer(
                user_id=new_user.id,
                first_name=other_info.first_name,
                last_name=other_info.last_name,
                birth_date=other_info.birth_date,
                phone_number=other_info.phone_number,
            )
            session.add(volunteer)
        elif user.user_type == UserType.ORGANISATION:
            organisation = Organisation(
                user_id=new_user.id,
                org_name=other_info.org_name,
                contact_person=other_info.contact_person,
                description=other_info.description,
                phone_number=other_info.phone_number,
                address=other_info.address,
                verified=other_info.verified,
            )
            session.add(organisation)
        elif user.user_type == UserType.COORDINATOR:
            coordinator = Coordinator(
                user_id=new_user.id,
                first_name=other_info.first_name,
                last_name=other_info.last_name,
                school=other_info.school,
                phone_number=other_info.phone_number,
                verified=other_info.verified,
            )
            session.add(coordinator)
        session.commit()
        session.refresh(new_user)
        return new_user

    except Exception:
        session.rollback()
        raise Exception("Błąd podczas dodawania użytkownika!")


def delete_user(session, user_id: int) -> bool:
    """
    Removes user and related data from db.

    :param session: SQLAlchemy Session
    :param user_id: ID of user to delete
    :return: True jeśli usunięto, False jeśli użytkownik nie istnieje
    """
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return False  # użytkownik nie istnieje

    try:
        # Usuń powiązane dane w zależności od typu użytkownika
        if user.user_type == UserType.VOLUNTEER:
            session.query(Volunteer).filter(Volunteer.user_id == user_id).delete()
        elif user.user_type == UserType.ORGANISATION:
            session.query(Organisation).filter(Organisation.user_id == user_id).delete()
        elif user.user_type == UserType.COORDINATOR:
            session.query(Coordinator).filter(Coordinator.user_id == user_id).delete()

        # Usuń użytkownika
        session.delete(user)
        session.commit()
        return True

    except Exception:
        session.rollback()
        raise Exception("Błąd podczas usuwania użytkownika!")

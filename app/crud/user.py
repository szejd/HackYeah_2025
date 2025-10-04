"""CRUD operations for User-related database operations."""

from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.db_models import User, Volunteer, Organisation, Coordinator
from app.schemas.enums import UserType
from app.models.user import (
    UserCreate,
    VolunteerCreate,
    VolunteerUpdate,
    OrganisationCreate,
    OrganisationUpdate,
    CoordinatorCreate,
    CoordinatorUpdate,
)


from sqlalchemy.orm import Session


# User CRUD Operations


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """
    Get a user by their ID.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID

    Returns:
        User object or None if not found
    """
    return session.query(User).filter(User.id == user_id).first()


def get_user_by_email(session: Session, email: str) -> User | None:
    """
    Get a user by their email address.

    Args:
        session: SQLAlchemy Session
        email: The user's email

    Returns:
        User object or None if not found
    """
    return session.query(User).filter(User.email == email).first()


def create_user(
    session: Session,
    user_data: UserCreate,
    password_hash: str,
    location_id: int | None = None,
) -> User:
    """
    Create a new base user.

    Args:
        session: SQLAlchemy Session
        user_data: User creation data
        password_hash: Hashed password
        location_id: Optional location ID

    Returns:
        Created User object

    Raises:
        IntegrityError: If email already exists
    """
    new_user = User(
        email=user_data.email,
        password_hash=password_hash,
        user_type=user_data.user_type,
        location_id=location_id,
    )
    try:
        session.add(new_user)
        session.flush()
        return new_user
    except IntegrityError:
        session.rollback()
        raise ValueError(f"User with email {user_data.email} already exists")


# Volunteer CRUD Operations


def create_volunteer(
    session: Session,
    user: User,
    volunteer_data: VolunteerCreate,
) -> Volunteer:
    """
    Create a new volunteer profile.

    Args:
        session: SQLAlchemy Session
        user: User object to associate with
        volunteer_data: Volunteer creation data

    Returns:
        Created Volunteer object
    """
    volunteer = Volunteer(
        user_id=user.id,
        first_name=volunteer_data.first_name,
        last_name=volunteer_data.last_name,
        birth_date=volunteer_data.birth_date,
        phone_number=volunteer_data.phone_number,
    )
    session.add(volunteer)
    return volunteer


def get_volunteer_by_user_id(session: Session, user_id: int) -> Volunteer | None:
    """
    Get a volunteer by their user ID.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID

    Returns:
        Volunteer object or None if not found
    """
    return session.query(Volunteer).filter(Volunteer.user_id == user_id).first()


# Organisation CRUD Operations


def create_organisation(
    session: Session,
    user: User,
    org_data: OrganisationCreate,
) -> Organisation:
    """
    Create a new organisation profile.

    Args:
        session: SQLAlchemy Session
        user: User object to associate with
        org_data: Organisation creation data

    Returns:
        Created Organisation object
    """
    organisation = Organisation(
        user_id=user.id,
        org_name=org_data.org_name,
        contact_person=org_data.contact_person,
        description=org_data.description,
        phone_number=org_data.phone_number,
        address=org_data.address,
        verified=org_data.verified,
    )
    session.add(organisation)
    return organisation


def get_organisation_by_user_id(session: Session, user_id: int) -> Organisation | None:
    """
    Get an organisation by their user ID.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID

    Returns:
        Organisation object or None if not found
    """
    return session.query(Organisation).filter(Organisation.user_id == user_id).first()


# Coordinator CRUD Operations


def create_coordinator(
    session: Session,
    user: User,
    coord_data: CoordinatorCreate,
) -> Coordinator:
    """
    Create a new coordinator profile.

    Args:
        session: SQLAlchemy Session
        user: User object to associate with
        coord_data: Coordinator creation data

    Returns:
        Created Coordinator object
    """
    coordinator = Coordinator(
        user_id=user.id,
        first_name=coord_data.first_name,
        last_name=coord_data.last_name,
        school=coord_data.school,
        phone_number=coord_data.phone_number,
        verified=coord_data.verified,
    )
    session.add(coordinator)
    return coordinator


def get_coordinator_by_user_id(session: Session, user_id: int) -> Coordinator | None:
    """
    Get a coordinator by their user ID.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID

    Returns:
        Coordinator object or None if not found
    """
    return session.query(Coordinator).filter(Coordinator.user_id == user_id).first()


# Update Operations


def update_volunteer(
    session: Session,
    user_id: int,
    volunteer_data: VolunteerUpdate,
) -> Volunteer | None:
    """
    Update volunteer profile information.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID
        volunteer_data: Volunteer update data (only fields to update)

    Returns:
        Updated Volunteer object or None if not found
    """
    volunteer = get_volunteer_by_user_id(session, user_id)
    if not volunteer:
        return None

    try:
        # Update only provided fields
        for field, value in volunteer_data.model_dump(exclude_unset=True).items():
            setattr(volunteer, field, value)

        session.commit()
        session.refresh(volunteer)
        return volunteer
    except Exception as e:
        session.rollback()
        raise ValueError(f"Failed to update volunteer: {str(e)}")


def update_organisation(
    session: Session,
    user_id: int,
    org_data: OrganisationUpdate,
) -> Organisation | None:
    """
    Update organisation profile information.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID
        org_data: Organisation update data (only fields to update)

    Returns:
        Updated Organisation object or None if not found
    """
    organisation = get_organisation_by_user_id(session, user_id)
    if not organisation:
        return None

    try:
        # Update only provided fields
        for field, value in org_data.model_dump(exclude_unset=True).items():
            setattr(organisation, field, value)

        session.commit()
        session.refresh(organisation)
        return organisation
    except Exception as e:
        session.rollback()
        raise ValueError(f"Failed to update organisation: {str(e)}")


def update_coordinator(
    session: Session,
    user_id: int,
    coord_data: CoordinatorUpdate,
) -> Coordinator | None:
    """
    Update coordinator profile information.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID
        coord_data: Coordinator update data (only fields to update)

    Returns:
        Updated Coordinator object or None if not found
    """
    coordinator = get_coordinator_by_user_id(session, user_id)
    if not coordinator:
        return None

    try:
        # Update only provided fields
        for field, value in coord_data.model_dump(exclude_unset=True).items():
            setattr(coordinator, field, value)

        session.commit()
        session.refresh(coordinator)
        return coordinator
    except Exception as e:
        session.rollback()
        raise ValueError(f"Failed to update coordinator: {str(e)}")


# Get User with Profile


def get_user_with_profile(session: Session, user_id: int) -> User | None:
    """
    Get a user with their complete profile (eagerly loads related data).

    This function loads the user and their type-specific profile
    (volunteer, organisation, or coordinator) in a single query.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID

    Returns:
        User object with profile loaded, or None if not found

    Example:
        >>> user = get_user_with_profile(db, 123)
        >>> if user and user.user_type == UserType.VOLUNTEER:
        >>>     print(user.volunteer.first_name)
    """
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    # Eagerly load the type-specific profile
    if user.user_type == UserType.VOLUNTEER:
        _ = user.volunteer  # Triggers lazy loading
    elif user.user_type == UserType.ORGANISATION:
        _ = user.organisation  # Triggers lazy loading
    elif user.user_type == UserType.COORDINATOR:
        _ = user.coordinator  # Triggers lazy loading

    return user


# Combined Registration Operations


def register_volunteer(
    session: Session,
    user_data: UserCreate,
    volunteer_data: VolunteerCreate,
    password_hash: str,
    location_id: int | None = None,
) -> tuple[User, Volunteer]:
    """
    Register a new volunteer (creates both User and Volunteer).

    Args:
        session: SQLAlchemy Session
        user_data: User creation data
        volunteer_data: Volunteer creation data
        password_hash: Hashed password
        location_id: Optional location ID

    Returns:
        Tuple of (User, Volunteer)

    Raises:
        ValueError: If user already exists or registration fails
    """
    try:
        # Ensure user type is volunteer
        user_data.user_type = UserType.VOLUNTEER

        # Create user
        user = create_user(session, user_data, password_hash, location_id)

        # Create volunteer profile
        volunteer = create_volunteer(session, user, volunteer_data)

        # Commit transaction
        session.commit()
        session.refresh(user)
        session.refresh(volunteer)

        return user, volunteer
    except Exception as e:
        session.rollback()
        raise ValueError(f"Failed to register volunteer: {str(e)}")


def register_organisation(
    session: Session,
    user_data: UserCreate,
    org_data: OrganisationCreate,
    password_hash: str,
    location_id: int | None = None,
) -> tuple[User, Organisation]:
    """
    Register a new organisation (creates both User and Organisation).

    Args:
        session: SQLAlchemy Session
        user_data: User creation data
        org_data: Organisation creation data
        password_hash: Hashed password
        location_id: Optional location ID

    Returns:
        Tuple of (User, Organisation)

    Raises:
        ValueError: If user already exists or registration fails
    """
    try:
        # Ensure user type is organisation
        user_data.user_type = UserType.ORGANISATION

        # Create user
        user = create_user(session, user_data, password_hash, location_id)

        # Create organisation profile
        organisation = create_organisation(session, user, org_data)

        # Commit transaction
        session.commit()
        session.refresh(user)
        session.refresh(organisation)

        return user, organisation
    except Exception as e:
        session.rollback()
        raise ValueError(f"Failed to register organisation: {str(e)}")


def register_coordinator(
    session: Session,
    user_data: UserCreate,
    coord_data: CoordinatorCreate,
    password_hash: str,
    location_id: int | None = None,
) -> tuple[User, Coordinator]:
    """
    Register a new coordinator (creates both User and Coordinator).

    Args:
        session: SQLAlchemy Session
        user_data: User creation data
        coord_data: Coordinator creation data
        password_hash: Hashed password
        location_id: Optional location ID

    Returns:
        Tuple of (User, Coordinator)

    Raises:
        ValueError: If user already exists or registration fails
    """
    try:
        # Ensure user type is coordinator
        user_data.user_type = UserType.COORDINATOR

        # Create user
        user = create_user(session, user_data, password_hash, location_id)

        # Create coordinator profile
        coordinator = create_coordinator(session, user, coord_data)

        # Commit transaction
        session.commit()
        session.refresh(user)
        session.refresh(coordinator)

        return user, coordinator
    except Exception as e:
        session.rollback()
        raise ValueError(f"Failed to register coordinator: {str(e)}")


def delete_user(session: Session, user_id: int) -> bool:
    """
    Delete a user and all associated data.

    Args:
        session: SQLAlchemy Session
        user_id: The user's ID

    Returns:
        True if deleted, False if user not found
    """
    user = get_user_by_id(session, user_id)
    if not user:
        return False

    try:
        session.delete(user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise ValueError(f"Failed to delete user: {str(e)}")

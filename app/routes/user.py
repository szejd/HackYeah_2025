"""User management routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.db_handler.db_connection import get_db
from app.models.user import (
    # Registration models
    VolunteerRegistration,
    OrganisationRegistration,
    CoordinatorRegistration,
    # Response models
    UserResponse,
    VolunteerResponse,
    OrganisationResponse,
    CoordinatorResponse,
    VolunteerProfile,
    OrganisationProfile,
    CoordinatorProfile,
    # Update models
    VolunteerUpdate,
    OrganisationUpdate,
    CoordinatorUpdate,
    # Login model
    UserLogin,
)
from app.crud.user import (
    # Registration
    register_volunteer,
    register_organisation,
    register_coordinator,
    # Read operations
    get_user_by_id,
    get_user_by_email,
    get_user_with_profile,
    get_volunteer_by_user_id,
    get_organisation_by_user_id,
    get_coordinator_by_user_id,
    # Update operations
    update_volunteer,
    update_organisation,
    update_coordinator,
    # Delete operations
    delete_user,
)
from app.schemas.enums import UserType

router = APIRouter(prefix="/users", tags=["users"])

# Dependency for database session
DBSession = Annotated[Session, Depends(get_db)]


# Helper function for password hashing (you should implement proper hashing)
def hash_password(password: str) -> str:
    """Hash password. TODO: Implement proper bcrypt/argon2 hashing."""
    # This is a placeholder - implement proper password hashing!
    import hashlib

    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password. TODO: Implement proper password verification."""
    return hash_password(plain_password) == hashed_password


# ==================== Registration Endpoints ====================


@router.post(
    "/register/volunteer",
    response_model=VolunteerProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new volunteer",
)
async def create_volunteer_account(
    registration: VolunteerRegistration,
    db: DBSession,
):
    """
    Register a new volunteer account.

    Creates both a User and Volunteer profile in a single transaction.
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, registration.user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        # Hash password
        password_hash = hash_password(registration.user.password)

        # Register volunteer
        user, volunteer = register_volunteer(
            session=db,
            user_data=registration.user,
            volunteer_data=registration.volunteer,
            password_hash=password_hash,
        )

        return VolunteerProfile(
            user=UserResponse.model_validate(user),
            volunteer=VolunteerResponse.model_validate(volunteer),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/register/organisation",
    response_model=OrganisationProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new organisation",
)
async def create_organisation_account(
    registration: OrganisationRegistration,
    db: DBSession,
):
    """
    Register a new organisation account.

    Creates both a User and Organisation profile in a single transaction.
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, registration.user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        # Hash password
        password_hash = hash_password(registration.user.password)

        # Register organisation
        user, organisation = register_organisation(
            session=db,
            user_data=registration.user,
            org_data=registration.organisation,
            password_hash=password_hash,
        )

        return OrganisationProfile(
            user=UserResponse.model_validate(user),
            organisation=OrganisationResponse.model_validate(organisation),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/register/coordinator",
    response_model=CoordinatorProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new coordinator",
)
async def create_coordinator_account(
    registration: CoordinatorRegistration,
    db: DBSession,
):
    """
    Register a new coordinator account.

    Creates both a User and Coordinator profile in a single transaction.
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, registration.user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        # Hash password
        password_hash = hash_password(registration.user.password)

        # Register coordinator
        user, coordinator = register_coordinator(
            session=db,
            user_data=registration.user,
            coord_data=registration.coordinator,
            password_hash=password_hash,
        )

        return CoordinatorProfile(
            user=UserResponse.model_validate(user),
            coordinator=CoordinatorResponse.model_validate(coordinator),
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ==================== Authentication Endpoints ====================


@router.post("/login", summary="User login")
async def login(credentials: UserLogin, db: DBSession):
    """
    Authenticate a user and return user information.

    TODO: Implement JWT token generation and return access token.
    """
    # Get user by email
    user = get_user_by_email(db, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # TODO: Generate JWT token here
    # For now, just return user info
    return {
        "message": "Login successful",
        "user": UserResponse.model_validate(user),
        # "access_token": "...",  # Add JWT token here
        # "token_type": "bearer",
    }


# ==================== Read Endpoints ====================


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
async def get_user(user_id: int, db: DBSession):
    """Get basic user information by ID."""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.model_validate(user)


@router.get(
    "/{user_id}/profile",
    summary="Get user profile",
)
async def get_user_profile(user_id: int, db: DBSession):
    """
    Get complete user profile including type-specific information.

    Returns different profile structures based on user type:
    - Volunteer: includes volunteer details
    - Organisation: includes organisation details
    - Coordinator: includes coordinator details
    """
    user = get_user_with_profile(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Return appropriate profile based on user type
    if user.user_type == UserType.VOLUNTEER:
        volunteer = get_volunteer_by_user_id(db, user_id)
        return VolunteerProfile(
            user=UserResponse.model_validate(user),
            volunteer=VolunteerResponse.model_validate(volunteer),
        )
    elif user.user_type == UserType.ORGANISATION:
        organisation = get_organisation_by_user_id(db, user_id)
        return OrganisationProfile(
            user=UserResponse.model_validate(user),
            organisation=OrganisationResponse.model_validate(organisation),
        )
    elif user.user_type == UserType.COORDINATOR:
        coordinator = get_coordinator_by_user_id(db, user_id)
        return CoordinatorProfile(
            user=UserResponse.model_validate(user),
            coordinator=CoordinatorResponse.model_validate(coordinator),
        )


# ==================== Update Endpoints ====================


@router.patch(
    "/{user_id}/volunteer",
    response_model=VolunteerProfile,
    summary="Update volunteer profile",
)
async def update_volunteer_profile(
    user_id: int,
    volunteer_data: VolunteerUpdate,
    db: DBSession,
):
    """
    Update volunteer profile information.

    Only provided fields will be updated (partial update).
    """
    # Verify user exists and is a volunteer
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.user_type != UserType.VOLUNTEER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a volunteer",
        )

    # Update volunteer
    volunteer = update_volunteer(db, user_id, volunteer_data)
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Volunteer profile not found",
        )

    return VolunteerProfile(
        user=UserResponse.model_validate(user),
        volunteer=VolunteerResponse.model_validate(volunteer),
    )


@router.patch(
    "/{user_id}/organisation",
    response_model=OrganisationProfile,
    summary="Update organisation profile",
)
async def update_organisation_profile(
    user_id: int,
    org_data: OrganisationUpdate,
    db: DBSession,
):
    """
    Update organisation profile information.

    Only provided fields will be updated (partial update).
    """
    # Verify user exists and is an organisation
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.user_type != UserType.ORGANISATION:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not an organisation",
        )

    # Update organisation
    organisation = update_organisation(db, user_id, org_data)
    if not organisation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organisation profile not found",
        )

    return OrganisationProfile(
        user=UserResponse.model_validate(user),
        organisation=OrganisationResponse.model_validate(organisation),
    )


@router.patch(
    "/{user_id}/coordinator",
    response_model=CoordinatorProfile,
    summary="Update coordinator profile",
)
async def update_coordinator_profile(
    user_id: int,
    coord_data: CoordinatorUpdate,
    db: DBSession,
):
    """
    Update coordinator profile information.

    Only provided fields will be updated (partial update).
    """
    # Verify user exists and is a coordinator
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.user_type != UserType.COORDINATOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is not a coordinator",
        )

    # Update coordinator
    coordinator = update_coordinator(db, user_id, coord_data)
    if not coordinator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator profile not found",
        )

    return CoordinatorProfile(
        user=UserResponse.model_validate(user),
        coordinator=CoordinatorResponse.model_validate(coordinator),
    )


# ==================== Delete Endpoints ====================


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
)
async def delete_user_account(user_id: int, db: DBSession):
    """
    Delete a user account and all associated data.

    This will cascade delete the user's type-specific profile
    (volunteer, organisation, or coordinator).
    """
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return None

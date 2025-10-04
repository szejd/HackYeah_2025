"""Pydantic models for User-related API requests and responses.

These models are used for data validation and serialization between
frontend and backend, and are NOT database models.
"""

from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime
from app.schemas.enums import UserType


# Base User Models (for API communication)


class UserBase(BaseModel):
    """Base user information shared across all user types."""

    email: EmailStr


class UserCreate(UserBase):
    """Model for creating a new user."""

    password: str
    user_type: UserType


class UserLogin(BaseModel):
    """Model for user login."""

    email: EmailStr
    password: str


class UserResponse(UserBase):
    """User information returned to frontend (without sensitive data)."""

    id: int
    user_type: UserType
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Volunteer Models


class VolunteerBase(BaseModel):
    """Base volunteer information."""

    first_name: str
    last_name: str
    birth_date: date
    phone_number: str


class VolunteerCreate(VolunteerBase):
    """Model for creating a volunteer (combined with UserCreate)."""

    pass


class VolunteerUpdate(BaseModel):
    """Model for updating volunteer information."""

    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    phone_number: str | None = None


class VolunteerResponse(VolunteerBase):
    """Volunteer information returned to frontend."""

    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# Organisation Models


class OrganisationBase(BaseModel):
    """Base organisation information."""

    org_name: str
    contact_person: str
    description: str
    phone_number: str
    address: str


class OrganisationCreate(OrganisationBase):
    """Model for creating an organisation."""

    verified: bool = False


class OrganisationUpdate(BaseModel):
    """Model for updating organisation information."""

    org_name: str | None = None
    contact_person: str | None = None
    description: str | None = None
    phone_number: str | None = None
    address: str | None = None
    verified: bool | None = None


class OrganisationResponse(OrganisationBase):
    """Organisation information returned to frontend."""

    id: int
    user_id: int
    verified: bool

    model_config = ConfigDict(from_attributes=True)


# Coordinator Models


class CoordinatorBase(BaseModel):
    """Base coordinator information."""

    first_name: str
    last_name: str
    phone_number: str
    school: str


class CoordinatorCreate(CoordinatorBase):
    """Model for creating a coordinator."""

    verified: bool = False


class CoordinatorUpdate(BaseModel):
    """Model for updating coordinator information."""

    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    school: str | None = None
    verified: bool | None = None


class CoordinatorResponse(CoordinatorBase):
    """Coordinator information returned to frontend."""

    id: int
    user_id: int
    verified: bool

    model_config = ConfigDict(from_attributes=True)


# Combined Registration Models


class VolunteerRegistration(BaseModel):
    """Complete volunteer registration model."""

    user: UserCreate
    volunteer: VolunteerCreate


class OrganisationRegistration(BaseModel):
    """Complete organisation registration model."""

    user: UserCreate
    organisation: OrganisationCreate


class CoordinatorRegistration(BaseModel):
    """Complete coordinator registration model."""

    user: UserCreate
    coordinator: CoordinatorCreate


# Complete User Profile Models


class VolunteerProfile(BaseModel):
    """Complete volunteer profile (user + volunteer info)."""

    user: UserResponse
    volunteer: VolunteerResponse


class OrganisationProfile(BaseModel):
    """Complete organisation profile (user + organisation info)."""

    user: UserResponse
    organisation: OrganisationResponse


class CoordinatorProfile(BaseModel):
    """Complete coordinator profile (user + coordinator info)."""

    user: UserResponse
    coordinator: CoordinatorResponse

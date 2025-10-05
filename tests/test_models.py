"""Tests for Pydantic models."""

import pytest
from datetime import date, datetime
from pydantic import ValidationError

from app.models.user import (
    UserBase,
    UserCreate,
    UserLogin,
    TokenResponse,
    UserResponse,
    VolunteerBase,
    VolunteerCreate,
    VolunteerUpdate,
    VolunteerResponse,
    OrganisationBase,
    OrganisationCreate,
    OrganisationUpdate,
    OrganisationResponse,
    CoordinatorBase,
    CoordinatorCreate,
    CoordinatorUpdate,
    CoordinatorResponse,
    VolunteerRegistration,
    OrganisationRegistration,
    CoordinatorRegistration,
    VolunteerProfile,
    OrganisationProfile,
    CoordinatorProfile,
)
from app.models.location import LocationData, AddLocation
from app.schemas.enums import UserType, LocationType, RegistrationStatus


class TestUserModels:
    """Tests for User-related models."""

    def test_user_base_valid(self):
        """Test UserBase model with valid email."""
        user = UserBase(email="test@example.com")
        assert user.email == "test@example.com"

    def test_user_base_invalid_email(self):
        """Test UserBase model with invalid email."""
        with pytest.raises(ValidationError) as exc_info:
            UserBase(email="invalid-email")
        assert "value is not a valid email address" in str(exc_info.value)

    def test_user_create_valid(self):
        """Test UserCreate model with valid data."""
        user = UserCreate(email="volunteer@example.com", password="securepass123", user_type=UserType.VOLUNTEER)
        assert user.email == "volunteer@example.com"
        assert user.password == "securepass123"
        assert user.user_type == UserType.VOLUNTEER

    def test_user_create_all_user_types(self):
        """Test UserCreate model with all user types."""
        for user_type in [UserType.VOLUNTEER, UserType.ORGANISATION, UserType.COORDINATOR]:
            user = UserCreate(email=f"{user_type}@example.com", password="pass123", user_type=user_type)
            assert user.user_type == user_type

    def test_user_login_valid(self):
        """Test UserLogin model with valid data."""
        login = UserLogin(email="user@example.com", password="mypassword")
        assert login.email == "user@example.com"
        assert login.password == "mypassword"

    def test_token_response_defaults(self):
        """Test TokenResponse model with default values."""
        user_response = UserResponse(
            id=1,
            email="test@example.com",
            user_type=UserType.VOLUNTEER,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        token = TokenResponse(access_token="token123", user=user_response)
        assert token.access_token == "token123"
        assert token.token_type == "bearer"
        assert token.success is False
        assert token.user == user_response

    def test_token_response_custom(self):
        """Test TokenResponse model with custom values."""
        user_response = UserResponse(
            id=1,
            email="test@example.com",
            user_type=UserType.VOLUNTEER,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        token = TokenResponse(access_token="token123", token_type="custom", user=user_response, success=True)
        assert token.token_type == "custom"
        assert token.success is True

    def test_user_response_from_attributes(self):
        """Test UserResponse model with from_attributes config."""
        now = datetime.now()
        user = UserResponse(
            id=1,
            email="test@example.com",
            user_type=UserType.VOLUNTEER,
            created_at=now,
            updated_at=now,
        )
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.user_type == UserType.VOLUNTEER
        assert user.created_at == now
        assert user.updated_at == now


class TestVolunteerModels:
    """Tests for Volunteer-related models."""

    def test_volunteer_base_valid(self):
        """Test VolunteerBase model with valid data."""
        volunteer = VolunteerBase(
            first_name="John",
            last_name="Doe",
            birth_date=date(1990, 1, 1),
            phone_number="+48123456789",
        )
        assert volunteer.first_name == "John"
        assert volunteer.last_name == "Doe"
        assert volunteer.birth_date == date(1990, 1, 1)
        assert volunteer.phone_number == "+48123456789"

    def test_volunteer_create_inherits_base(self):
        """Test VolunteerCreate model inherits from VolunteerBase."""
        volunteer = VolunteerCreate(
            first_name="Jane",
            last_name="Smith",
            birth_date=date(1995, 5, 15),
            phone_number="555-1234",
        )
        assert volunteer.first_name == "Jane"
        assert volunteer.last_name == "Smith"

    def test_volunteer_update_all_none(self):
        """Test VolunteerUpdate model with all None values."""
        update = VolunteerUpdate()
        assert update.first_name is None
        assert update.last_name is None
        assert update.birth_date is None
        assert update.phone_number is None

    def test_volunteer_update_partial(self):
        """Test VolunteerUpdate model with partial data."""
        update = VolunteerUpdate(first_name="NewName", phone_number="999-9999")
        assert update.first_name == "NewName"
        assert update.last_name is None
        assert update.birth_date is None
        assert update.phone_number == "999-9999"

    def test_volunteer_response_valid(self):
        """Test VolunteerResponse model with valid data."""
        volunteer = VolunteerResponse(
            id=1,
            user_id=10,
            first_name="John",
            last_name="Doe",
            birth_date=date(1990, 1, 1),
            phone_number="+48123456789",
        )
        assert volunteer.id == 1
        assert volunteer.user_id == 10


class TestOrganisationModels:
    """Tests for Organisation-related models."""

    def test_organisation_base_valid(self):
        """Test OrganisationBase model with valid data."""
        org = OrganisationBase(
            org_name="Test Charity",
            contact_person="Jane Manager",
            description="A test charity organisation",
            phone_number="+48987654321",
            address="123 Main St, City",
        )
        assert org.org_name == "Test Charity"
        assert org.contact_person == "Jane Manager"
        assert org.description == "A test charity organisation"
        assert org.phone_number == "+48987654321"
        assert org.address == "123 Main St, City"

    def test_organisation_create_default_verified(self):
        """Test OrganisationCreate model with default verified value."""
        org = OrganisationCreate(
            org_name="Test Org",
            contact_person="Person",
            description="Desc",
            phone_number="123",
            address="Addr",
        )
        assert org.verified is False

    def test_organisation_create_custom_verified(self):
        """Test OrganisationCreate model with custom verified value."""
        org = OrganisationCreate(
            org_name="Test Org",
            contact_person="Person",
            description="Desc",
            phone_number="123",
            address="Addr",
            verified=True,
        )
        assert org.verified is True

    def test_organisation_update_all_none(self):
        """Test OrganisationUpdate model with all None values."""
        update = OrganisationUpdate()
        assert update.org_name is None
        assert update.contact_person is None
        assert update.description is None
        assert update.phone_number is None
        assert update.address is None
        assert update.verified is None

    def test_organisation_update_partial(self):
        """Test OrganisationUpdate model with partial data."""
        update = OrganisationUpdate(org_name="New Org Name", verified=True)
        assert update.org_name == "New Org Name"
        assert update.verified is True
        assert update.contact_person is None

    def test_organisation_response_valid(self):
        """Test OrganisationResponse model with valid data."""
        org = OrganisationResponse(
            id=1,
            user_id=20,
            org_name="Test Org",
            contact_person="Contact",
            description="Description",
            phone_number="123",
            address="Address",
            verified=True,
        )
        assert org.id == 1
        assert org.user_id == 20
        assert org.verified is True


class TestCoordinatorModels:
    """Tests for Coordinator-related models."""

    def test_coordinator_base_valid(self):
        """Test CoordinatorBase model with valid data."""
        coord = CoordinatorBase(
            first_name="Alice", last_name="Coordinator", phone_number="+48111222333", school="Test School"
        )
        assert coord.first_name == "Alice"
        assert coord.last_name == "Coordinator"
        assert coord.phone_number == "+48111222333"
        assert coord.school == "Test School"

    def test_coordinator_create_default_verified(self):
        """Test CoordinatorCreate model with default verified value."""
        coord = CoordinatorCreate(
            first_name="Alice", last_name="Coordinator", phone_number="+48111222333", school="Test School"
        )
        assert coord.verified is False

    def test_coordinator_create_custom_verified(self):
        """Test CoordinatorCreate model with custom verified value."""
        coord = CoordinatorCreate(
            first_name="Alice",
            last_name="Coordinator",
            phone_number="+48111222333",
            school="Test School",
            verified=True,
        )
        assert coord.verified is True

    def test_coordinator_update_all_none(self):
        """Test CoordinatorUpdate model with all None values."""
        update = CoordinatorUpdate()
        assert update.first_name is None
        assert update.last_name is None
        assert update.phone_number is None
        assert update.school is None
        assert update.verified is None

    def test_coordinator_update_partial(self):
        """Test CoordinatorUpdate model with partial data."""
        update = CoordinatorUpdate(school="New School", verified=True)
        assert update.school == "New School"
        assert update.verified is True
        assert update.first_name is None

    def test_coordinator_response_valid(self):
        """Test CoordinatorResponse model with valid data."""
        coord = CoordinatorResponse(
            id=1,
            user_id=30,
            first_name="Alice",
            last_name="Coordinator",
            phone_number="+48111222333",
            school="Test School",
            verified=True,
        )
        assert coord.id == 1
        assert coord.user_id == 30
        assert coord.verified is True


class TestRegistrationModels:
    """Tests for combined registration models."""

    def test_volunteer_registration_valid(self):
        """Test VolunteerRegistration model with valid data."""
        registration = VolunteerRegistration(
            user=UserCreate(email="volunteer@test.com", password="pass123", user_type=UserType.VOLUNTEER),
            volunteer=VolunteerCreate(
                first_name="John",
                last_name="Doe",
                birth_date=date(1990, 1, 1),
                phone_number="123456789",
            ),
        )
        assert registration.user.email == "volunteer@test.com"
        assert registration.user.user_type == UserType.VOLUNTEER
        assert registration.volunteer.first_name == "John"

    def test_organisation_registration_valid(self):
        """Test OrganisationRegistration model with valid data."""
        registration = OrganisationRegistration(
            user=UserCreate(email="org@test.com", password="pass123", user_type=UserType.ORGANISATION),
            organisation=OrganisationCreate(
                org_name="Test Org",
                contact_person="Manager",
                description="Desc",
                phone_number="123",
                address="Addr",
            ),
        )
        assert registration.user.email == "org@test.com"
        assert registration.user.user_type == UserType.ORGANISATION
        assert registration.organisation.org_name == "Test Org"

    def test_coordinator_registration_valid(self):
        """Test CoordinatorRegistration model with valid data."""
        registration = CoordinatorRegistration(
            user=UserCreate(email="coord@test.com", password="pass123", user_type=UserType.COORDINATOR),
            coordinator=CoordinatorCreate(first_name="Alice", last_name="Coord", phone_number="123", school="School"),
        )
        assert registration.user.email == "coord@test.com"
        assert registration.user.user_type == UserType.COORDINATOR
        assert registration.coordinator.first_name == "Alice"


class TestProfileModels:
    """Tests for complete user profile models."""

    def test_volunteer_profile_valid(self):
        """Test VolunteerProfile model with valid data."""
        now = datetime.now()
        profile = VolunteerProfile(
            user=UserResponse(
                id=1,
                email="volunteer@test.com",
                user_type=UserType.VOLUNTEER,
                created_at=now,
                updated_at=now,
            ),
            volunteer=VolunteerResponse(
                id=1,
                user_id=1,
                first_name="John",
                last_name="Doe",
                birth_date=date(1990, 1, 1),
                phone_number="123456789",
            ),
        )
        assert profile.user.id == 1
        assert profile.volunteer.user_id == 1
        assert profile.user.user_type == UserType.VOLUNTEER

    def test_organisation_profile_valid(self):
        """Test OrganisationProfile model with valid data."""
        now = datetime.now()
        profile = OrganisationProfile(
            user=UserResponse(
                id=2,
                email="org@test.com",
                user_type=UserType.ORGANISATION,
                created_at=now,
                updated_at=now,
            ),
            organisation=OrganisationResponse(
                id=2,
                user_id=2,
                org_name="Test Org",
                contact_person="Manager",
                description="Desc",
                phone_number="123",
                address="Addr",
                verified=True,
            ),
        )
        assert profile.user.id == 2
        assert profile.organisation.user_id == 2
        assert profile.user.user_type == UserType.ORGANISATION

    def test_coordinator_profile_valid(self):
        """Test CoordinatorProfile model with valid data."""
        now = datetime.now()
        profile = CoordinatorProfile(
            user=UserResponse(
                id=3,
                email="coord@test.com",
                user_type=UserType.COORDINATOR,
                created_at=now,
                updated_at=now,
            ),
            coordinator=CoordinatorResponse(
                id=3,
                user_id=3,
                first_name="Alice",
                last_name="Coord",
                phone_number="123",
                school="School",
                verified=False,
            ),
        )
        assert profile.user.id == 3
        assert profile.coordinator.user_id == 3
        assert profile.user.user_type == UserType.COORDINATOR


class TestLocationModels:
    """Tests for Location-related models."""

    def test_location_data_valid(self):
        """Test LocationData model with valid coordinates."""
        location = LocationData(name="Test Location", latitude=52.2297, longitude=21.0122, category=LocationType.EVENT)
        assert location.name == "Test Location"
        assert location.latitude == 52.2297
        assert location.longitude == 21.0122
        assert location.category == LocationType.EVENT

    def test_location_data_all_categories(self):
        """Test LocationData model with all category types."""
        for category in [LocationType.VOLUNTEER, LocationType.ORGANISATION, LocationType.EVENT]:
            location = LocationData(name="Test", latitude=0.0, longitude=0.0, category=category)
            assert location.category == category

    def test_location_data_extreme_coordinates(self):
        """Test LocationData model with extreme valid coordinates."""
        # North pole
        location_north = LocationData(name="North", latitude=90.0, longitude=0.0, category=LocationType.EVENT)
        assert location_north.latitude == 90.0

        # South pole
        location_south = LocationData(name="South", latitude=-90.0, longitude=0.0, category=LocationType.EVENT)
        assert location_south.latitude == -90.0

        # International date line
        location_east = LocationData(name="East", latitude=0.0, longitude=180.0, category=LocationType.EVENT)
        assert location_east.longitude == 180.0

        location_west = LocationData(name="West", latitude=0.0, longitude=-180.0, category=LocationType.EVENT)
        assert location_west.longitude == -180.0

    def test_location_data_out_of_range_coordinates(self):
        """Test LocationData model accepts coordinates outside typical range (no validation)."""
        # Note: The model doesn't validate coordinate ranges, so these should pass
        location = LocationData(name="Invalid", latitude=91.0, longitude=0.0, category=LocationType.EVENT)
        assert location.latitude == 91.0

        location = LocationData(name="Invalid", latitude=-91.0, longitude=0.0, category=LocationType.EVENT)
        assert location.latitude == -91.0

        location = LocationData(name="Invalid", latitude=0.0, longitude=181.0, category=LocationType.EVENT)
        assert location.longitude == 181.0

        location = LocationData(name="Invalid", latitude=0.0, longitude=-181.0, category=LocationType.EVENT)
        assert location.longitude == -181.0

    def test_add_location_valid(self):
        """Test AddLocation model with valid data."""
        add_loc = AddLocation(address="123 Test Street, City", location_name="Test Venue")
        assert add_loc.address == "123 Test Street, City"
        assert add_loc.location_name == "Test Venue"


class TestEnums:
    """Tests for enum types."""

    def test_user_type_enum_values(self):
        """Test UserType enum has correct values."""
        assert UserType.VOLUNTEER == "volunteer"
        assert UserType.ORGANISATION == "organisation"
        assert UserType.COORDINATOR == "coordinator"

    def test_user_type_enum_membership(self):
        """Test UserType enum membership."""
        assert "volunteer" in [e.value for e in UserType]
        assert "organisation" in [e.value for e in UserType]
        assert "coordinator" in [e.value for e in UserType]

    def test_location_type_enum_values(self):
        """Test LocationType enum has correct values."""
        assert LocationType.VOLUNTEER == "volunteer"
        assert LocationType.ORGANISATION == "organisation"
        assert LocationType.EVENT == "event"

    def test_location_type_enum_membership(self):
        """Test LocationType enum membership."""
        assert "volunteer" in [e.value for e in LocationType]
        assert "organisation" in [e.value for e in LocationType]
        assert "event" in [e.value for e in LocationType]

    def test_registration_status_enum(self):
        """Test RegistrationStatus enum."""
        assert hasattr(RegistrationStatus, "PENDING")
        assert hasattr(RegistrationStatus, "CONFIRMED")
        assert RegistrationStatus.PENDING.name == "PENDING"
        assert RegistrationStatus.CONFIRMED.name == "CONFIRMED"


class TestModelValidation:
    """Tests for model validation edge cases."""

    def test_email_validation_various_formats(self):
        """Test email validation with various formats."""
        valid_emails = [
            "test@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com",
        ]
        for email in valid_emails:
            user = UserBase(email=email)
            assert user.email == email

    def test_email_validation_invalid_formats(self):
        """Test email validation rejects invalid formats."""
        invalid_emails = [
            "invalid",
            "@example.com",
            "user@",
            "user @example.com",
            "user@example",
        ]
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                UserBase(email=email)

    def test_birth_date_validation(self):
        """Test birth date validation."""
        # Valid dates
        valid_dates = [
            date(1990, 1, 1),
            date(2000, 12, 31),
            date(1950, 6, 15),
        ]
        for birth_date in valid_dates:
            volunteer = VolunteerBase(first_name="John", last_name="Doe", birth_date=birth_date, phone_number="123")
            assert volunteer.birth_date == birth_date

    def test_missing_required_fields(self):
        """Test validation fails when required fields are missing."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(email="test@example.com")  # type: ignore  # Missing password and user_type
        errors = exc_info.value.errors()
        field_names = [error["loc"][0] for error in errors]
        assert "password" in field_names
        assert "user_type" in field_names

    def test_extra_fields_ignored(self):
        """Test that extra fields are handled according to model config."""
        # By default, Pydantic ignores extra fields
        user_data = {
            "email": "test@example.com",
            "password": "pass123",
            "user_type": UserType.VOLUNTEER,
            "extra_field": "ignored",
        }
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert not hasattr(user, "extra_field")

    def test_type_validation_strict(self):
        """Test that Pydantic v2 uses strict type validation."""
        # Pydantic v2 doesn't auto-coerce int to string by default
        with pytest.raises(ValidationError) as exc_info:
            VolunteerBase(
                first_name="John",
                last_name="Doe",
                birth_date=date(1990, 1, 1),
                phone_number=123456789,  # type: ignore
            )
        errors = exc_info.value.errors()
        assert any(error["loc"][0] == "phone_number" for error in errors)

    def test_optional_fields_none(self):
        """Test optional fields can be None."""
        update = VolunteerUpdate(first_name="NewName")
        assert update.first_name == "NewName"
        assert update.last_name is None
        assert update.birth_date is None
        assert update.phone_number is None

    def test_model_serialization(self):
        """Test model can be serialized to dict."""
        user = UserCreate(email="test@example.com", password="pass123", user_type=UserType.VOLUNTEER)
        user_dict = user.model_dump()
        assert user_dict["email"] == "test@example.com"
        assert user_dict["password"] == "pass123"
        assert user_dict["user_type"] == "volunteer"

    def test_model_json_serialization(self):
        """Test model can be serialized to JSON."""
        now = datetime.now()
        user = UserResponse(
            id=1,
            email="test@example.com",
            user_type=UserType.VOLUNTEER,
            created_at=now,
            updated_at=now,
        )
        json_str = user.model_dump_json()
        assert "test@example.com" in json_str
        assert "volunteer" in json_str

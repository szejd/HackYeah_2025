from enum import StrEnum, Enum, auto


class UserType(StrEnum):
    VOLUNTEER = "volunteer"
    ORGANISATION = "organisation"
    COORDINATOR = "coordinator"


class LocationType(StrEnum):
    VOLUNTEER = "volunteer"
    ORGANISATION = "organisation"
    EVENT = "event"


class RegistrationStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()


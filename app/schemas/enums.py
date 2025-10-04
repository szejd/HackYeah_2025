from enum import StrEnum


class UserType(StrEnum):
    VOLUNTEER = "volunteer"
    ORGANISATION = "organisation"
    COORDINATOR = "coordinator"


class LocationType(StrEnum):
    VOLUNTEER = "volunteer"
    ORGANISATION = "organisation"
    EVENT = "event"

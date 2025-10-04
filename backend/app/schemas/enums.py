from enum import Enum


class UserType(Enum):
    VOLUNTEER = "volunteer"
    ORGANISATION = "organisation"
    COORDINATOR = "coordinator"

class LocationType(Enum):
    VOLUNTEER = "volunteer"
    ORGANISATION = "organisation"
    EVENT = "event"

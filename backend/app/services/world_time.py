from typing import TypedDict

from app.utils.time_utils import get_time_in_timezone


class WorldTimeInfo(TypedDict):
    """Structure for world time information."""

    city: str
    timezone: str
    current_time: str


WORLD_CITIES: dict[str, str] = {
    "New York": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Warsaw": "Europe/Warsaw",
}


def get_world_times() -> list[WorldTimeInfo]:
    """
    Return a list of {city, timezone, current_time}.
    This is where you'd add DB calls or external APIs if needed.
    """
    return [
        WorldTimeInfo(city=city, timezone=tz, current_time=get_time_in_timezone(tz))
        for city, tz in WORLD_CITIES.items()
    ]

from datetime import datetime
from typing import Final
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Constants for time formatting and error messages
DATETIME_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
INVALID_TIMEZONE_MESSAGE: Final[str] = "Invalid timezone"


def get_time_in_timezone(timezone_name: str) -> str:
    """
    Return the current time in the given timezone as a formatted string.

    Args:
        timezone_name: The name of the timezone (e.g., 'America/New_York', 'UTC')

    Returns:
        A formatted datetime string in the format YYYY-MM-DD HH:MM:SS,
        or an error message if the timezone is invalid.
    """
    try:
        tz = ZoneInfo(timezone_name)
        now = datetime.now(tz)
        return now.strftime(DATETIME_FORMAT)
    except ZoneInfoNotFoundError:
        return INVALID_TIMEZONE_MESSAGE

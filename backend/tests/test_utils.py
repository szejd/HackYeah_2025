from backend.app.utils.time_utils import get_time_in_timezone


def test_get_time_in_timezone():
    assert get_time_in_timezone("Asia/Kolkata")


def test_get_time_in_timezone_invalid():
    result = get_time_in_timezone("random_zone")
    assert result == "Invalid timezone"

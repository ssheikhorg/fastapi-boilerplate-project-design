"""Helper functions for the bot."""
from datetime import datetime, timezone

datetime_now = str(datetime.today().replace(microsecond=0, tzinfo=timezone.utc))[0:19]
datetime_dt_fmt = datetime.today().replace(microsecond=0, tzinfo=timezone.utc)


def timestamp_to_datetime(timestamp: int) -> str:
    """Converts a timestamp to a datetime object."""
    return str(datetime.fromtimestamp(timestamp).replace(microsecond=0))


def str_datetime_to_datetime(str_datetime: str) -> datetime:
    """Converts a datetime string to a datetime object."""
    return datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")

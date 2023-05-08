"""Helper functions for the bot."""
from datetime import datetime, timezone, timedelta
from random import choice
from string import ascii_letters, digits
from typing import Any

datetime_now = str(datetime.today().replace(microsecond=0, tzinfo=timezone.utc))[0:19]
datetime_dt_fmt = datetime.today().replace(microsecond=0, tzinfo=timezone.utc)


def timestamp_to_datetime(timestamp: int) -> str:
    """Converts a timestamp to a datetime object."""
    return str(datetime.fromtimestamp(timestamp).replace(microsecond=0))


def str_datetime_to_datetime(str_datetime: str) -> datetime:
    """Converts a datetime string to a datetime object."""
    return datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")


def generate_random_string(length: int) -> str:
    """Generates a random string."""
    return "".join(choice(ascii_letters + digits) for _ in range(length))


def generate_random_integers(length: int) -> str:
    """Generates a random string of integers."""
    return "".join(choice(digits) for _ in range(length))


def generate_time_delta(
        days: int = None, hours: int = None, minutes: int = None,
        seconds: int = None, fmt: str = "%Y-%m-%d %H:%M:%S"
) -> Any:
    """Generates a time delta."""
    datetime_result: Any = None
    if days:
        datetime_result = datetime_dt_fmt - timedelta(days=days)
    if hours:
        datetime_result = datetime_dt_fmt - timedelta(hours=hours)
    if minutes:
        datetime_result = datetime_dt_fmt - timedelta(minutes=minutes)
    if seconds:
        datetime_result = datetime_dt_fmt - timedelta(seconds=seconds)
    if datetime_result:
        datetime_result = datetime_result.strftime(fmt)
    return datetime_result


def generate_weekly_formatted_date(_from: str, _to: str) -> list:
    """Generates a formatted date for the weekly command starts from every tuesday."""
    start_weekday = datetime.strptime(_from, "%Y-%m-%d")
    end_weekday = datetime.strptime(_to, "%Y-%m-%d")
    start_year, start_week_num, start_day_of_week = start_weekday.isocalendar()
    end_year, end_week_num, end_day_of_week = end_weekday.isocalendar()

    start_dt = datetime.strptime(f"{start_year}-W{start_week_num}-{1}", "%Y-W%W-%w")
    _dates = datetime.strptime(f"{end_year}-W{end_week_num}-{1}", "%Y-W%W-%w")
    end_dt = _dates + timedelta(days=7, seconds=-1)

    # see the week difference between the start and end date
    week_diff = (end_dt - start_dt).days // 7
    weeks_dt = []
    # push every week date into a list
    for i in range(week_diff + 1):
        _start = start_dt + timedelta(days=7 * i)
        _end = _start + timedelta(days=7, seconds=-1)
        weeks_dt.append({"start": _start, "end": _end, "week_number": _start.isocalendar()[1]})

    return weeks_dt

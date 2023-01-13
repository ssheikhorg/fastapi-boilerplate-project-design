from datetime import datetime

datetime_now = datetime.today().replace(microsecond=0)


def timestamp_to_datetime(timestamp: int) -> datetime:
    return datetime.fromtimestamp(timestamp).replace(microsecond=0)

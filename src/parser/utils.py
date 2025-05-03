import time
from datetime import datetime, timedelta, timezone


def yield_lines(filename: str):
    """
    This acts as a fixed interface to yield lines from the log file
    Particularly useful if the implementation on how to read the lines needs
    to change in the future, from a static file to a data strem
    """
    for line in open_and_yield_line(filename=filename):
        yield line


def open_and_yield_line(filename: str):
    with open(filename, "r") as f:
        for line in f:
            yield line


def datetime_isoformat_to_timestamp(
    datetime_str: str, timedelta_min: float = 0.0
) -> float:
    delta = timedelta(minutes=timedelta_min)
    dt = datetime.fromisoformat(datetime_str) + delta
    ts = dt.timestamp()
    return ts


def datetime_to_isoformat(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%S%z")


def sleep_until(target_time=datetime) -> float:
    now_tz = datetime.now(timezone.utc)
    sleep_in_sec = (target_time - now_tz).total_seconds()
    if sleep_in_sec > 0:
        time.sleep(sleep_in_sec)
        return sleep_in_sec

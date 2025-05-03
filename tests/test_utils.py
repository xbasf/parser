from datetime import datetime, timedelta, timezone
from math import isclose
from parser.utils import (
    datetime_isoformat_to_timestamp,
    datetime_to_isoformat,
    sleep_until,
)
from unittest.mock import patch

import pytest


def test_datetime_isoformat_to_timestamp():

    datetime_str = "20250430T120000+01"
    timedelta_min = 3.0
    expected_timestamp = 1746010980

    ts = datetime_isoformat_to_timestamp(
        datetime_str=datetime_str, timedelta_min=timedelta_min
    )

    assert ts == expected_timestamp


@pytest.mark.parametrize(
    "dt_input, expected_isoformat",
    [
        (
            datetime.fromisoformat("20250429T200015+0100"),
            "20250429T200015+0100",
        ),
        (datetime.fromisoformat("20250420T100500+00"), "20250420T100500+0000"),
    ],
)
def test_datetime_to_isoformat(dt_input: datetime, expected_isoformat: str):
    dt = datetime_to_isoformat(dt=dt_input)
    assert dt == expected_isoformat


@patch("time.sleep", return_value=None)
@pytest.mark.parametrize(
    "target_dt, expected_sec_slept",
    [
        (datetime.now(timezone.utc) - timedelta(hours=1), None),
        (datetime.now(timezone.utc) + timedelta(hours=1), 60 * 60),
    ],
)
def test_sleep_until(
    patched_time_sleep, target_dt: datetime, expected_sec_slept: float
):
    seconds_slept = sleep_until(target_time=target_dt)
    if expected_sec_slept is None:
        assert seconds_slept == expected_sec_slept
    else:
        assert isclose(seconds_slept, expected_sec_slept, abs_tol=0.8)

from parser.model import TargetHost
from parser.stats import get_connection_counts, get_most_connected_hosts
from unittest.mock import mock_open, patch

import pytest

FILE_CONTENTS = """56556.0 host7 host1
56560.0 host61 host1
56570.0 host6 host1
56575.0 host6 host1
56580.0 host6 host1
56590.0 host7 host1"""

COUNTS_MASTER = {"host10": 9, "host7": 2}
COUNTS_SLAVE = {"host3": 10, "host7": 5}


@pytest.fixture
def my_host():
    return TargetHost(name="host1", output_folder="path")


def test_get_connection_counts(my_host):
    mocked_open = mock_open(read_data=FILE_CONTENTS)
    expected_counts = {"host6": 3, "host7": 2, "host61": 1}
    with patch("builtins.open", mocked_open):
        counts = get_connection_counts(host=my_host, connection_kind="slave")
    for actual, expected in zip(counts, expected_counts):
        assert actual == expected


def test_get_most_connected_hosts(my_host):
    expected_return = {"host3": 10}
    with patch("parser.stats.get_connection_counts") as mocked_func:
        mocked_func.side_effect = [COUNTS_MASTER, COUNTS_SLAVE]
        most_connected_hosts = get_most_connected_hosts(host=my_host)
    assert most_connected_hosts == expected_return

# from parser.main import list_slave_connections
from parser.main import list_slave_connections
from unittest.mock import mock_open, patch

FILE_CONTENTS = """1704072476 host20 host1
1704072480 host21 host1
1704072490 host2 host11
1704072500 host1 host2
1704072510 host24 host1
1704072520 host25 host2
1704072530 host24 host1
1704072540 host21 host1
1704072550 host20 host1
1704152417 host21 host1
"""


def test_list_slave_connections():
    mocked_open = mock_open(read_data=FILE_CONTENTS)
    expected_slave_list = ["host24", "host24", "host21", "host20"]
    with patch("builtins.open", mocked_open):
        out_slave_list = list_slave_connections(
            log_filename="my_file.log",
            target_hostname="host1",
            time_init="20240101T022830+01",
            time_end="20240101T022910+01",
            log_tolerance="1",
        )
        assert out_slave_list == expected_slave_list

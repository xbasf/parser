import os
from parser.model import ConnectionModel, TargetHost

import pytest


@pytest.fixture
def my_host():
    return TargetHost(name="host1", output_folder="test")


@pytest.fixture
def connection_a():
    return ConnectionModel(
        timestamp=12345, master={"name": "host1"}, slave={"name": "host2"}
    )


def test_target_host(my_host, connection_a):
    assert my_host.slave_conn_filepath == os.path.join(
        "test", "slave_connections.log"
    )
    assert my_host.master_conn_filepath == os.path.join(
        "test", "master_connections.log"
    )
    my_host.add_slave_connection(connection_a)
    assert my_host.slave_list == ["host2"]
    my_host.add_slave_connection(connection_a)
    assert my_host.slave_list == ["host2", "host2"]


def test_connection_model_from_to_line(connection_a):
    connection = ConnectionModel.from_log_line(connection_a.to_log_line())
    assert connection == connection_a

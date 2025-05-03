import json
import os
from typing import Dict, Literal

try:
    from .model import ConnectionModel, TargetHost
except ImportError:
    from model import ConnectionModel, TargetHost


def get_most_connected_hosts(host: TargetHost):
    """
    This finds the hostname with most master connections to the given host and
    the hostname with most slave connections to the given host. The hostname
    with the higher number of connections overall is returned.
    In case of a tie when deciding who is the most connected host, this just
    picks one.
    """
    empty_counts = {"none": 0}
    try:
        counts_master = get_connection_counts(
            host=host, connection_kind="master"
        )
    except FileNotFoundError:
        counts_master = empty_counts
    try:
        counts_slave = get_connection_counts(host=host, connection_kind="slave")
    except FileNotFoundError:
        counts_slave = empty_counts
    if counts_master == counts_slave == empty_counts:
        return
    most_connected_master = list(counts_master)[0]
    most_connected_slave = list(counts_slave)[0]
    if counts_master != empty_counts:
        print(
            f"host that recieved most connections from {host.name} at period {os.path.basename(host.output_folder)} is {most_connected_master}"
        )
    if counts_slave != empty_counts:
        print(
            f"host most connected to {host.name} at period {os.path.basename(host.output_folder)} is {most_connected_slave}"
        )
    most_connected_host, connections_count = (
        (most_connected_master, counts_master[most_connected_master])
        if counts_master[most_connected_master]
        >= counts_slave[most_connected_slave]
        else (most_connected_slave, counts_slave[most_connected_slave])
    )
    print(
        f"host that generated most connections at period {os.path.basename(host.output_folder)} is {most_connected_host} with {connections_count} connections"
    )
    return {most_connected_host: connections_count}


def get_connection_counts(
    host: TargetHost, connection_kind: Literal["slave", "master"]
) -> Dict[str, str]:
    """
    This computes the counts of either slave or master connections. The counts
    are represented in a dictionary being the host name as key and the count
    as value. The dictiory is sorted in descending order based on the value.
    The counts are stored in the host.output_folder as a .txt file
    """
    counts = {}
    for connection in ConnectionModel.from_log_file(
        filename=getattr(host, connection_kind + "_conn_filepath")
    ):
        counts[getattr(connection, connection_kind).name] = (
            counts.get(getattr(connection, connection_kind).name, 0) + 1
        )
    counts = {
        k: v
        for k, v in sorted(
            counts.items(), key=lambda item: item[1], reverse=True
        )
    }
    with open(
        os.path.join(
            host.output_folder, connection_kind + "_connections_counts.txt"
        ),
        "w",
    ) as f:
        json.dump(counts, f)
    return counts

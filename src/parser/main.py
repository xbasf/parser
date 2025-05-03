import os
from datetime import datetime, timedelta, timezone
from typing import List, Literal

try:  # local imports for the cli
    from .model import ConfigModel, ConnectionModel, TargetHost
    from .stats import get_most_connected_hosts
    from .utils import (
        datetime_isoformat_to_timestamp,
        datetime_to_isoformat,
        sleep_until,
    )
except ImportError:  # absolute imports for running the script
    from model import ConfigModel, ConnectionModel, TargetHost
    from stats import get_most_connected_hosts
    from utils import (
        datetime_isoformat_to_timestamp,
        datetime_to_isoformat,
        sleep_until,
    )


def find_connections(
    log_filename: str,
    target: TargetHost,
    target_method_names: List[
        Literal[
            "add_slave_connection",
            "save_slave_connection",
            "save_master_connection",
        ]
    ],
    time_init: str,
    time_end: str,
    log_tolerance: str = "5",
):
    """
    This finds the connections out of the log file that are connected to or
    from the target host (the given host) within the period time defined by
    time_init and time_end. The found connections are stored or added to the
    target host class instance.
    """
    ts_init = datetime_isoformat_to_timestamp(time_init)
    ts_end = datetime_isoformat_to_timestamp(time_end)
    ts_terminate = datetime_isoformat_to_timestamp(
        time_end, float(log_tolerance)
    )
    print(f"timestamp_init: {ts_init}\ntimestamp_end: {ts_end}")
    for connection in ConnectionModel.from_log_file(filename=log_filename):
        if connection.timestamp > ts_terminate:
            break
        if ts_init <= connection.timestamp <= ts_end:
            for target_method_name in target_method_names:
                target_method = getattr(target, target_method_name)
                target_method(connection)
    return target


def list_slave_connections(
    log_filename: str,
    target_hostname: str,
    time_init: str,
    time_end: str,
    log_tolerance: str,
):
    """
    This calls the function that finds the connections out of the log file and
    asks to keep them in memory. With the found connections it asks to
    retrieve the list of hosts connected to the target host (the given host)
    """
    target = TargetHost(name=target_hostname)
    print(f"target hostname: {target.name}")
    target = find_connections(
        log_filename=log_filename,
        target=target,
        target_method_names=["add_slave_connection"],
        time_init=time_init,
        time_end=time_end,
        log_tolerance=log_tolerance,
    )
    return target.slave_list


def save_all_connections(
    log_filename: str,
    output_folder: str,
    target_hostname: str,
    time_init: str,
    time_end: str,
    log_tolerance: str,
):
    """
    This calls the function that finds the connections out the log file and
    asks to save them to file
    """
    target = TargetHost(name=target_hostname)
    print(f"target hostname: {target_hostname}")
    target.output_folder = output_folder
    target = find_connections(
        log_filename=log_filename,
        target=target,
        target_method_names=["save_slave_connection", "save_master_connection"],
        time_init=time_init,
        time_end=time_end,
        log_tolerance=log_tolerance,
    )
    return target


def continuous_run(config_file: str = "config.yaml"):
    """
    This runs indefinitely. It makes use of the config_file and calls the
    functions that collect and save host connections and the functions that
    compute the stats
    """
    config = ConfigModel.from_yaml(filename=config_file)
    if config.time_init is None:
        now_tz = datetime.now(timezone(timedelta(hours=1)))
        time_init = datetime_to_isoformat(now_tz)
    else:
        time_init = datetime_to_isoformat(
            datetime.fromisoformat(config.time_init)
        )
    delta = timedelta(minutes=config.output_frequency_float)
    while True:
        time_end = datetime.fromisoformat(time_init) + delta
        time_end = datetime_to_isoformat(time_end)
        output_subfolder = time_init
        _ = sleep_until(
            target_time=datetime.fromisoformat(time_end)
            + timedelta(minutes=config.log_tolerance_float)
        )
        output_directory = os.path.join(config.output_folder, output_subfolder)
        os.makedirs(output_directory, exist_ok=True)
        target = save_all_connections(
            log_filename=config.log_filename,
            output_folder=output_directory,
            target_hostname=config.target_hostname,
            time_init=time_init,
            time_end=time_end,
            log_tolerance=config.log_tolerance,
        )
        _ = get_most_connected_hosts(host=target)
        time_init = time_end


if __name__ == "__main__":
    slave_list = list_slave_connections(
        "data/connectionsALL.log",
        "host40",
        "20240102T063550+01",
        "20240104004500+01",
        "5",
    )
    print(slave_list)

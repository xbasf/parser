import os
from typing import List, Optional

import yaml
from pydantic import BaseModel, computed_field

try:
    from .utils import yield_lines
except ImportError:
    from utils import yield_lines


class HostModel(BaseModel):
    name: str


class ConnectionModel(BaseModel):
    timestamp: float
    slave: HostModel
    master: HostModel

    @classmethod
    def from_log_line(cls, line: str):
        elements = line.split()
        return cls(
            timestamp=float(elements[0]),
            slave={"name": elements[1]},
            master={"name": elements[2]},
        )

    @classmethod
    def from_log_file(cls, filename: str):
        for line in yield_lines(filename=filename):
            yield cls.from_log_line(line)

    def to_log_line(self) -> str:
        return f"{self.timestamp} {self.slave.name} {self.master.name}"

    def append_to_log_file(self, filename: str):
        with open(filename, "a") as f:
            f.write(self.to_log_line() + "\n")


class TargetHost(HostModel):
    slave_connections: List[ConnectionModel] = list()
    output_folder: str = None

    def add_slave_connection(self, connection: ConnectionModel):
        if self.name == connection.master.name:
            print(f"slave connection appended: {connection}")
            self.slave_connections.append(connection)
        return self

    def save_slave_connection(self, connection: ConnectionModel):
        if self.name == connection.master.name:
            print(f"slave connection saved: {connection}")
            connection.append_to_log_file(self.slave_conn_filepath)
        return self

    def save_master_connection(self, connection: ConnectionModel):
        if self.name == connection.slave.name:
            print(f"master connection saved: {connection}")
            connection.append_to_log_file(self.master_conn_filepath)
        return self

    @computed_field
    @property
    def slave_list(self) -> List[str]:
        slaves = [
            slave_connection.slave.name
            for slave_connection in self.slave_connections
        ]
        return slaves

    @computed_field
    @property
    def slave_conn_filepath(self) -> str:
        if self.output_folder is not None:
            return os.path.join(self.output_folder, "slave_connections.log")

    @computed_field
    @property
    def master_conn_filepath(self) -> str:
        if self.output_folder is not None:
            return os.path.join(self.output_folder, "master_connections.log")


class ConfigModel(BaseModel):
    log_filename: str
    log_tolerance: str
    target_hostname: str
    time_init: Optional[str]
    output_folder: str
    output_frequency: str

    @classmethod
    def from_yaml(cls, filename: str):
        with open(filename, "r") as stream:
            config = yaml.safe_load(stream)
            return cls(**config)

    @computed_field
    @property
    def log_tolerance_float(self) -> float:
        return float(self.log_tolerance)

    @computed_field
    @property
    def output_frequency_float(self) -> float:
        return float(self.output_frequency)

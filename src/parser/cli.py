import os
import typer
from typing_extensions import Annotated

try:
    from .main import continuous_run, list_slave_connections
except ImportError:
    from parser.main import continuous_run, list_slave_connections

app = typer.Typer()


@app.command(
    help="prints a list of slave hostnames connected to the given hostname "
    "within a datetime range"
)
def list_slave_hosts(
    filename: Annotated[
        str, typer.Argument(help="filename with filepath to the log data")
    ],
    hostname: Annotated[str, typer.Argument(help="the given hostname")],
    time_init: Annotated[
        str,
        typer.Argument(
            help="initial datetime expressed in ISO 8601 format e.g. "
            "YYYYMMDDThhmmss+00 T is a separator, +00 is the time offset in "
            "hours from UTC"
        ),
    ],
    time_end: Annotated[
        str,
        typer.Argument(
            help="end datetime expressed in ISO 8601 format YYYYMMDDThhmmss+00 "
            "T is a separator, +00 is the time offset in hours from UTC"
        ),
    ],
    tolerance: Annotated[
        str,
        typer.Argument(
            help="Time in minutes a line in the filename can be out of order "
            "by"
        ),
    ] = "5",
):
    slave_connections = list_slave_connections(
        log_filename=filename,
        target_hostname=hostname,
        time_init=time_init,
        time_end=time_end,
        log_tolerance=tolerance,
    )
    print(slave_connections)


@app.command(
    help="continuous run, periodically captures both slave and master "
    "hostnames connected to the given hostname, computes the connection "
    "counts and finds out the most connected host to or from the given "
    "hostname"
)
def run_continuously(
    config_file: Annotated[
        str, typer.Argument(help="YAML config filename with filepath")
    ] = f"{os.path.join('src','parser','config.yaml')}",
):
    continuous_run(config_file=config_file)


if __name__ == "__main__":
    app()

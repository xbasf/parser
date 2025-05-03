# Parser

## Installation

Create a venv called venv

```
python -m venv venv
```

Activate the venv - if running windows

```
.venv\Scripts\activate
```

pip install requirements file

```
pip install -r requiremtnes.txt
```

pip install the module in editable mode

```
pip install -e .
```

## Usage

This comes with a CLI application, to run it, simply call the package and the command you may wish to execute. For a list of all the available commands run the application's help

```
parser --help
```

## Naming convention

|name|description|example|
|---|---|---|
|connection|connection from a host (left) to another host (right) at a given time|`1711337192 host3 host1`|
|target host|the given hostname|`host1`|
|slave host|host connected to the target host|`host3`|
|slave connection|connection where the slave host is connected to the target host|`1711337192 host3 host1`|
|master host|host that received a connection from the target host|`host5`|
|master connection|connection where the target host is connected to the master host|`1711337192 host1 host5`|


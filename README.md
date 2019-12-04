# click-option-group

[![PyPI version](https://img.shields.io/pypi/v/click-option-group.svg)](https://pypi.python.org/pypi/click-option-group)
[![Build status](https://travis-ci.org/espdev/click-option-group.svg?branch=master)](https://travis-ci.org/espdev/click-option-group)
![Supported Python versions](https://img.shields.io/pypi/pyversions/click-option-group.svg)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


**click-option-group** is a Click-extension package that adds option groups 
missing in [Click](https://github.com/pallets/click/).

## The aim and motivation

Click is a package for creating powerful and beautiful command line interfaces (CLI) in Python, 
but it has no functionality for creating option groups.

Option groups are convenient mechanism for logical structuring CLI, also it allows you to set 
specific behavior and set the relation between options (mutually exclusive options for example). 
Moreover, [argparse](https://docs.python.org/3/library/argparse.html) stdlib package contains this 
functionality out of the box.

At the same time, many Click users need this functionality.
You can read interesting discussions about it in the following issues:

* [issue 257](https://github.com/pallets/click/issues/257)
* [issue 509](https://github.com/pallets/click/issues/509)
* [issue 1137](https://github.com/pallets/click/issues/1137)

The aim of this package is to provide group options extensible functionality 
using canonical and clean API (Click-like API as far as possible).

## Quickstart

### Installing 

Install and update using pip:

```bash
$ pip install click-option-group
```

### A Simple Example

Here is a simple example how to use option groups in your Click-based CLI.
Just use `optgroup` for decorating your cli-function in Click-like API style.

```python
# app.py

import click
from click_option_group import optgroup, MutuallyExclusiveOptionGroup


@click.command()
@optgroup.group('Server configuration', 
                help='The configuration of some server connection')
@optgroup.option('-h', '--host', default='localhost', help='Server host name')
@optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
@optgroup.option('-n', '--attempts', type=int, default=3, help='The number of connection attempts')
@optgroup.option('-t', '--timeout', type=int, default=30, help='The server response timeout')
@optgroup.group('Input data sources', cls=MutuallyExclusiveOptionGroup, required=True, 
                help='The sources of the input data')
@optgroup.option('--tsv-file', type=click.File(), help='CSV/TSV input data file')
@optgroup.option('--json-file', type=click.File(), help='JSON input data file')
@click.option('--debug/--no-debug', default=False, help='Debug flag')
def cli(**params):
    print(params)

if __name__ == '__main__':
    cli()
```

```bash
$ python app.py --help
Usage: app.py [OPTIONS]

Options:
  Server configuration:           The configuration of some server connection
    -h, --host TEXT               Server host name
    -p, --port INTEGER            Server port
    -n, --attempts INTEGER        The number of connection attempts
    -t, --timeout INTEGER         The server response timeout
  Input data sources: [mutually_exclusive, required]
                                  The sources of the input data
    --tsv-file FILENAME           CSV/TSV input data file
    --json-file FILENAME          JSON input data file
  --debug / --no-debug            Debug flag
  --help                          Show this message and exit.
```

### How it works

Firstly, we define the group:
```python
@optgroup.group('Server configuration', help='The configuration of some server connection')
```

Also we can define groups just using `optgroup()`:
```python
@optgroup('Server configuration', help='The configuration of some server connection')
```

Secondly, we add the options to the group:
```python
@optgroup.option('-h', '--host', default='localhost', help='Server host name')
@optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
```

The important point: do not mix `optgroup.option` and `click.option` decorators!

An incorrect code example:
```python
@optgroup.group('Server configuration', 
                help='The configuration of some server connection')
@click.option('--foo')  # ERROR
@optgroup.option('-h', '--host', default='localhost', help='Server host name')
@click.option('--bar')  # ERROR
@optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
```

The correct code looks like:
```python
@click.option('--foo')
@optgroup.group('Server configuration', 
                help='The configuration of some server connection')
@optgroup.option('-h', '--host', default='localhost', help='Server host name')
@optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
@click.option('--bar')
```

click-option-group checks the decorators order and raises the exception if `optgroup.option` and `click.option` are mixed.

Also if we will use `optgroup.option` without `optgroup.grpup()`/`optgroup()` it also raises exception.

An incorrect code example:
```python
@click.command()
@click.option('--foo')
@optgroup.option('-h', '--host', default='localhost', help='Server host name')  # ERROR: Missing declaration of the group
@optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
@click.option('--bar')
def cli(**params):
    pass
```

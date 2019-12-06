# click-option-group

[![PyPI version](https://img.shields.io/pypi/v/click-option-group.svg)](https://pypi.python.org/pypi/click-option-group)
[![Build status](https://travis-ci.org/espdev/click-option-group.svg?branch=master)](https://travis-ci.org/espdev/click-option-group)
[![Coverage Status](https://coveralls.io/repos/github/espdev/click-option-group/badge.svg?branch=master)](https://coveralls.io/github/espdev/click-option-group?branch=master)
![Supported Python versions](https://img.shields.io/pypi/pyversions/click-option-group.svg)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


**click-option-group** is a Click-extension package that adds option groups 
missing in [Click](https://github.com/pallets/click/).

## Aim and Motivation

Click is a package for creating powerful and beautiful command line interfaces (CLI) in Python, 
but it has no the functionality for creating option groups.

Option groups are convenient mechanism for logical structuring CLI, also it allows you to set 
the specific behavior and set the relationship among grouped options (mutually exclusive options for example). 
Moreover, [argparse](https://docs.python.org/3/library/argparse.html) stdlib package contains this 
functionality out of the box.

At the same time, many Click users need this functionality.
You can read interesting discussions about it in the following issues:

* [issue 257](https://github.com/pallets/click/issues/257)
* [issue 509](https://github.com/pallets/click/issues/509)
* [issue 1137](https://github.com/pallets/click/issues/1137)

The aim of this package is to provide group options with extensible functionality 
using canonical and clean API (Click-like API as far as possible).

## Quickstart

### Installing 

Install and update using pip:

```bash
$ pip install click-option-group
```

### A Simple Example

Here is a simple example how to use option groups in your Click-based CLI.
Just use `optgroup` for declaring option groups by decorating 
your command function in Click-like API style.

```python
# app.py

import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

@click.command()
@optgroup.group('Server configuration', 
                help='The configuration of some server connection')
@optgroup.option('-h', '--host', default='localhost', help='Server host name')
@optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
@optgroup.option('-n', '--attempts', type=int, default=3, help='The number of connection attempts')
@optgroup.option('-t', '--timeout', type=int, default=30, help='The server response timeout')
@optgroup.group('Input data sources', cls=RequiredMutuallyExclusiveOptionGroup, 
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

### How It Works

Firstly, we declare the group:
```python
@optgroup.group('Server configuration', help='The configuration of some server connection')
```

Also we can declare groups just using `optgroup()`:
```python
@optgroup('Server configuration', help='The configuration of some server connection')
```

Secondly, we declare the grouped options below:
```python
@optgroup.option('-h', '--host', default='localhost', help='Server host name')
@optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
```

### Checking Declarations

The important point: do not mix `optgroup.option` and `click.option` decorators!

**click-option-group** checks the decorators order and raises 
the exception if `optgroup.option` and `click.option` are mixed.

The following code is incorrect:
```python
@optgroup.group('My group')
@click.option('--hello')  # ERROR
@optgroup.option('--foo')
@click.option('--spam')  # ERROR
@optgroup.option('--bar')
```

The correct code looks like:
```python
@click.option('--hello')
@optgroup.group('My group')
@optgroup.option('--foo')
@optgroup.option('--bar')
@click.option('--spam')
```

If we try to use `optgroup.option` without `optgroup.grpup()`/`optgroup()` declaration 
it also will raise the exception.

The following code is incorrect:
```python
@click.command()
@click.option('--hello')
@optgroup.option('--foo')  # ERROR: Missing declaration of the option group
@optgroup.option('--bar')  # ERROR: Missing declaration of the option group
@click.option('--spam')
def cli(**params):
    pass
```

If we declare only option group without the options it will raise warning.

```python
@click.command()
@click.option('--hello')
@optgroup.group('My group')  # WARN: The empty option group
@click.option('--spam')
def cli(**params):
    pass
```

## API Features

Besides `optgroup` based decorators the package offers another way 
to declare grouped options using `OptionGroup` based class objects directly.
We can use the instances of these classes and use its `option` method as decorator for 
declaring and adding options to the group.

Here is an example how it looks:
```python
import click
from click_option_group import OptionGroup, RequiredMutuallyExclusiveOptionGroup

server_config = OptionGroup('Server configuration', help='The configuration of some server connection')
input_sources = RequiredMutuallyExclusiveOptionGroup('Input data sources', help='The sources of the input data')

@click.command()
@server_config.option('-h', '--host', default='localhost', help='Server host name')
@server_config.option('-p', '--port', type=int, default=8888, help='Server port')
@input_sources.option('--tsv-file', type=click.File(), help='CSV/TSV input data file')
@input_sources.option('--json-file', type=click.File(), help='JSON input data file')
@click.option('--debug/--no-debug', default=False, help='Debug flag')
def cli(**params):
    print(params)

if __name__ == '__main__':
    cli()
```

In this case initially we create group objects and then we use `option` method for 
declaring options.

As well as in above example we cannot mix `option` and `click.option` decorators.
The following code is incorrect and will raise the exception:
```python
@server_config.option('-h', '--host', default='localhost', help='Server host name')
@click.option('--foo')  # ERROR
@server_config.option('-p', '--port', type=int, default=8888, help='Server port')
@input_sources.option('--tsv-file', type=click.File(), help='CSV/TSV input data file')
@click.option('--bar')  # ERROR
@input_sources.option('--json-file', type=click.File(), help='JSON input data file')
```

## Behavior and Relationship among Options

The groups are useful to define the specific behavior and relationship among grouped options.

**click-option-groups** offers two main classes: `OptionGroup` and `GroupedOption`.
 
`OptionGroup` and `GroupedOption` classes contain the main functionality for support option groups. 
They do not contain the specific behavior or relationship among grouped options.
 
The specific behavior can be implemented by using the inheritance, mainly, in `OptionGroup` sub classes.
**click-option-groups** offers some useful `OptionGroup` based classes out of the box:
- `RequiredAnyOptionGroup` -- At least one option from the group must be set.
- `RequiredAllOptionGroup` --  All options from the group must be set.
- `MutuallyExclusiveOptionGroup` -- Only one or none option from the group must be set 
- `RequiredMutuallyExclusiveOptionGroup` -- Only one required option from the group must be set

`OptionGroup` based class can be specified via `cls` argument in `optgroup()`/`optgroup.group()` decorator or
can be used directly when the second method is used.

If you want to implement some complex behavior you can create a sub class of `GroupedOption` class and use
your `GroupedOption` based class via `cls` argument in `optgroup.option`/`OptionGroup.option` decorator method.

## Limitations

The package does not support nested option groups. This is intentional.
Nested option groups complicate the implementation, API and CLI and most often it is not necessary.

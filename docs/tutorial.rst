.. _tutorial:

Tutorial
========

A Simple Example
----------------

.. currentmodule:: click_option_group

Let's start with a simple example. Just use :class:`optgroup` for declaring option groups
by decorating your command function in Click-like API style.

.. code-block:: python

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

Now we can see help for our app::

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

How It Works
------------

Firstly, we declare the group using :func:`optgroup.group` decorator:

.. code-block:: python

    @optgroup.group('Server configuration', help='The configuration of some server connection')

.. note::

    Also we can declare groups just using ``optgroup()``:

    .. code-block:: python

        @optgroup('Server configuration', help='The configuration of some server connection')

Secondly, we declare the grouped options below using :func:`optgroup.option` decorator:

.. code-block:: python

    @optgroup.option('-h', '--host', default='localhost', help='Server host name')
    @optgroup.option('-p', '--port', type=int, default=8888, help='Server port')

And that is all!

Checking Declarations
---------------------

.. attention::

    The important point: do not mix :func:`optgroup.option` and :func:`click.option` decorators!

**click-option-group** checks the decorators order and raises
the exception if :func:`optgroup.option` and :func:`click.option` decorators are mixed.

The following code is incorrect:

.. code-block:: python

    @optgroup.group('My group')
    @click.option('--hello')  # ERROR
    @optgroup.option('--foo')
    @click.option('--spam')  # ERROR
    @optgroup.option('--bar')

The correct code looks like:

.. code-block:: python

    @click.option('--hello')
    @optgroup.group('My group')
    @optgroup.option('--foo')
    @optgroup.option('--bar')
    @click.option('--spam')


If we try to use ``optgroup.option`` without ``optgroup.grpup()``/``optgroup()``
declaration it also will raise the exception.

The following code is incorrect:

.. code-block:: python

    @click.command()
    @click.option('--hello')
    @optgroup.option('--foo')  # ERROR: Missing declaration of the option group
    @optgroup.option('--bar')  # ERROR: Missing declaration of the option group
    @click.option('--spam')
    def cli(**params):
        pass

If we declare only option group without the options it will raise warning.

.. code-block:: python

    @click.command()
    @click.option('--hello')
    @optgroup.group('My group')  # WARN: The empty option group
    @click.option('--spam')
    def cli(**params):
        pass

API Features
------------

Besides :class:`optgroup` based decorators the package offers another way
to declare grouped options using :class:`OptionGroup` based class objects directly.
We can use the instances of these classes and use its :func:`OptionGroup.option` method as
decorator for declaring and adding options to the group.

Here is an example how it looks:

.. code-block:: python

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

In this case initially we create group objects and then we use :func:`OptionGroup.option` method for
declaring options.

As well as in above example we cannot mix ``option`` and ``click.option`` decorators.
The following code is incorrect and will raise the exception:

.. code-block:: python

    @server_config.option('-h', '--host', default='localhost', help='Server host name')
    @click.option('--foo')  # ERROR
    @server_config.option('-p', '--port', type=int, default=8888, help='Server port')
    @input_sources.option('--tsv-file', type=click.File(), help='CSV/TSV input data file')
    @click.option('--bar')  # ERROR
    @input_sources.option('--json-file', type=click.File(), help='JSON input data file')


Behavior and Relationship among Options
---------------------------------------

The groups are useful to define the specific behavior and relationship among grouped options.

**click-option-groups** provides two main classes: :class:`OptionGroup` and :class:`GroupedOption`.

- :class:`OptionGroup` class is a new entity for Click that provides the abstraction for grouping options and manage it.
- :class:`GroupedOption` class is inherited from :class:`click.Option` and provides the functionality for grouped options.

:class:`OptionGroup` and :class:`GroupedOption` classes contain the basic functionality for support option groups.
Both these classes do not contain the specific behavior or relationship among grouped options.

The specific behavior can be implemented by using the inheritance, mainly, in :class:`OptionGroup` sub classes.
**click-option-groups** provides some useful :class:`OptionGroup` based classes out of the box:

- :class:`RequiredAnyOptionGroup` -- At least one option from the group must be set
- :class:`AllOptionGroup` --  All options from the group must be set or none must be set
- :class:`RequiredAllOptionGroup` --  All options from the group must be set
- :class:`MutuallyExclusiveOptionGroup` -- Only one or none option from the group must be set
- :class:`RequiredMutuallyExclusiveOptionGroup` -- Only one required option from the group must be set

:class:`OptionGroup` based class can be specified via ``cls`` argument in ``optgroup()``/``optgroup.group()``
decorator or can be used directly when the second API way is used.

If you want to implement some complex behavior you can create a sub class of `GroupedOption` class and use
your :class:`GroupedOption` based class via ``cls`` argument in ``optgroup.option``/``OptionGroup.option``
decorator method:

.. code-block:: python

    @click.command()
    @optgroup('My group', cls=MyCustomOptionGroup)
    @optgroup.option('--foo', cls=MyCustomGroupedOption)
    ...

Limitations
-----------

The package does not support nested option groups (option subgroups). This is intentional.
Nested option groups complicate the implementation, API and CLI and most often it is not necessary.

If you think you need to nested option groups try redesign your CLI and doing it with
`nesting commands <https://click.palletsprojects.com/quickstart/#nesting-commands>`_.

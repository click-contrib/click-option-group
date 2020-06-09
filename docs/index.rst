.. click-option-group documentation master file, created by
   sphinx-quickstart on Sat Jan 18 02:32:05 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

click-option-group
==================

**click-option-group** is a `Click <https://click.palletsprojects.com>`_-extension package
that adds option groups missing in Click.

Aim and Motivation
------------------

Click is a package for creating powerful and beautiful command line interfaces (CLI) in Python,
but it has no the functionality for creating option groups.

Option groups are convenient mechanism for logical structuring CLI, also it allows you to set
the specific behavior and set the relationship among grouped options (mutually exclusive options for example).
Moreover, `argparse <https://docs.python.org/3/library/argparse.html>`_ stdlib package contains this
functionality out of the box.

At the same time, many Click users need this functionality.
You can read interesting discussions about it in the following issues:

* `issue 257 <https://github.com/pallets/click/issues/257>`_
* `issue 373 <https://github.com/pallets/click/issues/373>`_
* `issue 509 <https://github.com/pallets/click/issues/509>`_
* `issue 1137 <https://github.com/pallets/click/issues/1137>`_

The aim of this package is to provide group options with extensible functionality
using canonical and clean API (Click-like API as far as possible).

Installing
----------

You can install and update click-option-group using pip::

   pip install -U click-option-group

Quickstart
----------

Here is a simple example how to use option groups in your Click-based CLI.

.. code-block:: python

    import click
    from click_option_group import optgroup

    @click.command()
    @optgroup.group('Server configuration',
                    help='The configuration of some server connection')
    @optgroup.option('-h', '--host', default='localhost', help='Server host name')
    @optgroup.option('-p', '--port', type=int, default=8888, help='Server port')
    @click.option('--debug/--no-debug', default=False, help='Debug flag')
    def cli(host, port, debug):
         print(params)

    if __name__ == '__main__':
        cli()


Contents
--------

.. toctree::
   :maxdepth: 2

   tutorial
   api
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

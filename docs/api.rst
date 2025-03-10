.. _api:

API Reference
=============

.. currentmodule:: click_option_group

.. autosummary::
    :nosignatures:

    optgroup

    GroupedOption
    OptionGroup

    RequiredAnyOptionGroup
    AllOptionGroup
    RequiredAllOptionGroup
    MutuallyExclusiveOptionGroup
    RequiredMutuallyExclusiveOptionGroup

|

.. py:class:: optgroup

    A global instance of the helper class to manage creating groups and group options via decorators

    The class provides two decorator-methods: ``group``/``__call__`` and ``option``.
    These decorators should be used for adding grouped options. The class have
    single global instance ``optgroup`` that should be used in most cases.

    The example of usage::

        from click_option_group import optgroup

        ...
        @optgroup('Group 1', help='option group 1')
        @optgroup.option('--foo')
        @optgroup.option('--bar')
        @optgroup.group('Group 2', help='option group 2')
        @optgroup.option('--spam')
        ...

    .. py:method:: group(name, *, cls, help, **attrs)

        The decorator creates a new group and collects its options

        Creates the option group and registers all grouped options
        which were added by :func:`option` decorator.

        :param name: Group name or None for default name
        :param cls: Option group class that should be inherited from :class:`OptionGroup` class
        :param help: Group help or None for empty help
        :param attrs: Additional parameters of option group class

    .. py:method:: option(*param_decls, **attrs)

        The decorator adds a new option to the group

        The decorator is lazy. It adds option decls and attrs.
        All options will be registered by :func:`group` decorator.

        :param param_decls: option declaration tuple
        :param attrs: additional option attributes and parameters

----

.. autoclass:: GroupedOption
    :members:

----

.. autoclass:: OptionGroup
    :members:

----

.. autoclass:: RequiredAnyOptionGroup
    :members:

----

.. autoclass:: AllOptionGroup
    :members:

----

.. autoclass:: RequiredAllOptionGroup
    :members:

----

.. autoclass:: MutuallyExclusiveOptionGroup
    :members:

----

.. autoclass:: RequiredMutuallyExclusiveOptionGroup
    :members:

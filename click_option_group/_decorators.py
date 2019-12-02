# -*- coding: utf-8 -*-

import typing as ty
import collections.abc as abc
import collections
import warnings

import click

from ._core import OptionGroup
from ._helpers import (
    get_callback_and_params,
    get_fake_option_name,
    raise_mixing_decorators_error,
)


class OptionStackItem(ty.NamedTuple):
    param_decls: ty.Tuple[str, ...]
    attrs: ty.Dict[str, ty.Any]
    param_count: int


class _NotAttachedOption(click.Option):

    def __init__(self, param_decls=None, *, option_decls, all_options, **attrs):
        super().__init__(param_decls, expose_value=False, **attrs)
        self.option_decls = option_decls
        self._all_options = all_options

    def handle_parse_result(self, ctx, opts, args):
        self._raise_error(ctx)

    def get_help_record(self, ctx):
        self._raise_error(ctx)

    def _raise_error(self, ctx):
        options_error_hint = ''
        for option in reversed(self._all_options[ctx.command.callback]):
            decls = option.option_decls
            options_error_hint += f'  {click.Option(decls).get_error_hint(ctx)}\n'
        options_error_hint = options_error_hint[:-1]

        raise click.ClickException((
            f"The following grouped options were not attached to some option group:\n"
            f"{options_error_hint}\n"
            "Add @optgroup.group('Group name') decorator above to create a group."))


class _OptGroup:
    """A helper class to manage creating groups and group options via decorators

    The class provides two decorator-methods: `group`/`__call__` and `option`.
    These decorators should be used for adding grouped options. The class have
    single global instance `optgroup` that should be used in most cases.

    The example of usage::

        ...
        @optgroup('Group 1', help='option group 1')
        @optgroup.option('--foo')
        @optgroup.option('--bar')
        @optgroup.group('Group 2', help='option group 2')
        @optgroup.option('--spam')
        ...

    """

    def __init__(self) -> None:
        self._decorating_state: ty.Dict[abc.Callable, ty.List[OptionStackItem]] = collections.defaultdict(list)
        self._not_attached_options: ty.Dict[abc.Callable, ty.List[click.Option]] = collections.defaultdict(list)

    def __call__(self, name: ty.Optional[str] = None, help: ty.Optional[str] = None,
                 cls: ty.Optional[ty.Type[OptionGroup]] = None, **attrs):
        return self.group(name, help, cls, **attrs)

    def group(self, name: ty.Optional[str] = None, help: ty.Optional[str] = None,
              cls: ty.Optional[ty.Type[OptionGroup]] = None, **attrs):
        """The decorator creates a new group and collects its options

        :param name: Group name or None for deault name
        :param help: Group help or None for empty help
        :param cls: Option group class that should be inherited from `OptionGroup` class
        :param attrs: Additional parameters of option group class

        """

        if not cls:
            cls = OptionGroup
        else:
            if not issubclass(cls, OptionGroup):
                raise TypeError("'cls' must be a subclass of 'OptionGroup' class.")

        def decorator(func):
            callback, params = get_callback_and_params(func)

            if callback not in self._decorating_state:
                with_name = f' "{name}"' if name else ''
                warnings.warn(
                    f'There is attempt to add an empty option group{with_name}. The group will not be added.',
                    UserWarning)
                return func

            option_stack = self._decorating_state[callback]
            self._check_mixing_decorators(option_stack, params)

            option_group = cls(name, help, **attrs)

            for item in option_stack:
                func = option_group.option(*item.param_decls, **item.attrs)(func)

            del option_stack
            del self._decorating_state[callback]

            for opt in self._not_attached_options[callback]:
                params.remove(opt)
            del self._not_attached_options[callback]

            return func

        return decorator

    def option(self, *param_decls, **attrs):
        """The decorator adds a new option to the group

        :param param_decls: option declaration tuple
        :param attrs: additional option attributes and parameters

        """

        def decorator(func):
            callback, params = get_callback_and_params(func)
            option_stack = self._decorating_state[callback]

            self._check_mixing_decorators(option_stack, params)
            self._add_not_attached_option(func, param_decls)
            option_stack.append(OptionStackItem(param_decls, attrs, len(params)))

            return func

        return decorator

    def _add_not_attached_option(self, func, param_decls):
        click.option(f'{get_fake_option_name()}',
                     option_decls=param_decls,
                     all_options=self._not_attached_options,
                     cls=_NotAttachedOption)(func)

        callback, params = get_callback_and_params(func)
        self._not_attached_options[callback].append(params[-1])

    @staticmethod
    def _check_mixing_decorators(options_stack, params):
        if options_stack:
            last_state = options_stack[-1]
            if len(params) > last_state.param_count:
                raise_mixing_decorators_error(params[-1])


optgroup = _OptGroup()
"""Decorator creates groups of options and adds options into groups
"""

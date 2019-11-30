# -*- coding: utf-8 -*-

import warnings
import weakref
import typing as ty

import click
from click.core import augment_usage_errors


class GroupedOption(click.Option):
    """Represents grouped (related) optional values
    """

    def __init__(self, param_decls=None, *, group: 'OptionGroup', **attrs):
        super().__init__(param_decls, **attrs)
        self.__group = weakref.ref(group)

    @property
    def group(self) -> 'OptionGroup':
        return self.__group()

    def handle_parse_result(self, ctx, opts, args):
        with augment_usage_errors(ctx, param=self):
            self.group.before_handle_parse_result(self, ctx, opts)
        return super().handle_parse_result(ctx, opts, args)


class OptionGroup:
    """Represents the abstraction for grouped (related) options
    """

    def __init__(self, name: ty.Optional[str] = None, *, requied: bool = False) -> None:
        self._name = name if name else ''
        self._requied = requied

        self._command = None
        self._options = {}

    @property
    def name(self) -> str:
        """Returns the group name or empty string if it was not set

        :return: group name
        """
        return self._name

    @property
    def required(self) -> bool:
        """Returns 'required' flag

        If 'required' is True, at least one option from the group must be set.

        :return: required flag
        """
        return self._requied

    def option(self, *param_decls, **attrs):
        """Decorator attaches an grouped option to the command
        """
        def decorator(func):
            option_attrs = attrs.copy()

            self._ignore_argument('required', option_attrs)
            option_attrs.setdefault('cls', GroupedOption)

            if not issubclass(option_attrs['cls'], GroupedOption):
                raise TypeError("'cls' argument must be a subclass of 'GroupedOption' class.")

            if self._command:
                if func is not self._command:
                    raise ValueError(f"Option group '{self}' is already used for '{self._command}'.")
            else:
                self._command = func

            func = click.option(*param_decls, group=self, **option_attrs)(func)
            self._option_memo(func)
            return func

        return decorator

    def before_handle_parse_result(self, option: GroupedOption, ctx: click.Context, opts: dict) -> None:
        self.check_required(
            'At least one option from the following option group is required', option, ctx, opts)

    def check_required(self, message, option, ctx, opts):
        if not self.required:
            return
        if option.name in opts:
            return
        if not set(self._options).intersection(opts):
            error_text = f'{message}:\n'

            if self.name:
                error_text += f'{self.name}:'

            for group_opt in self._options.values():
                error_text += f'\n  {group_opt.get_error_hint(ctx)}'

            raise click.UsageError(error_text, ctx=ctx)

    @staticmethod
    def _ignore_argument(name: str, attrs: dict):
        if name in attrs:
            del attrs[name]
            warnings.warn(f"'{name}' argument is ignored for group's option.",
                          UserWarning, stacklevel=2)

    def _option_memo(self, func):
        if isinstance(func, click.Command):
            option: click.Option = func.params[-1]
        else:
            option: click.Option = func.__click_params__[-1]

        self._options[option.name] = option

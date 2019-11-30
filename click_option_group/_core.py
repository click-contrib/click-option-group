# -*- coding: utf-8 -*-

import typing as ty
import warnings
import weakref

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
        """Returns the group for this option

        :return: [OptionGroup] the group for this option
        """
        return self.__group()

    def handle_parse_result(self, ctx, opts, args):
        with augment_usage_errors(ctx, param=self):
            self.group.handle_parse_result(self, ctx, opts)
        return super().handle_parse_result(ctx, opts, args)


class OptionGroup:
    """Option group manages grouped (related) options
    """

    def __init__(self, name: ty.Optional[str] = None, *, requied: bool = False) -> None:
        self._name = name if name else ''
        self._requied = requied
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

            func = click.option(*param_decls, group=self, **option_attrs)(func)
            self._option_memo(func)
            return func

        return decorator

    def handle_parse_result(self, option: GroupedOption, ctx: click.Context, opts: dict) -> None:
        if not self.required:
            return
        if option.name in opts:
            return

        options = self._get_options(ctx)

        if not set(options).intersection(opts):
            error_text = 'At least one option from the following option group is required:'
            if self.name:
                error_text += f'\n{self.name}:'

            for opt in options.values():
                error_text += f'\n  {opt.get_error_hint(ctx)}'

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
            func = func.callback
        else:
            option: click.Option = func.__click_params__[-1]

        self._options.setdefault(func, {})[option.name] = option

    def _get_options(self, ctx):
        return self._options.get(ctx.command.callback, {})


class MutuallyExclusiveOptionGroup(OptionGroup):
    """Option group with mutually exclusive behavior for grouped options
    """

    def handle_parse_result(self, option: GroupedOption, ctx: click.Context, opts: dict) -> None:
        options = self._get_options(ctx)
        given_option_names = set(options).intersection(opts)

        if self.required and not given_option_names:
            error_text = f'One required option must be set from the mutually exclusive option group:'
            if self.name:
                error_text += f'\n{self.name}:'

            for option in options.values():
                opt_err_hint = option.get_error_hint(ctx)
                error_text += f'\n  {opt_err_hint}'

            raise click.UsageError(error_text, ctx=ctx)

        if len(given_option_names) > 1:
            error_text = f'The given mutually exclusive options cannot be used at the same time:'

            for opt_name in given_option_names:
                opt_err_hint = options[opt_name].get_error_hint(ctx)
                error_text += f'\n  {opt_err_hint}'

            raise click.UsageError(error_text, ctx=ctx)

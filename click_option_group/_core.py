# -*- coding: utf-8 -*-

import typing as ty
import weakref

import click
from click.core import augment_usage_errors


class GroupedOption(click.Option):
    """Represents grouped (related) optional values
    """

    _forbidden_attrs = (
        'required',
    )

    def __init__(self, param_decls=None, *, group: 'OptionGroup', **attrs):
        for attr in self._forbidden_attrs:
            if attr in attrs:
                raise TypeError(f"'{attr}' attribute is not allowed for '{type(self).__name__}'.")

        self.__group = weakref.ref(group)
        super().__init__(param_decls, **attrs)

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

    def get_help_record(self, ctx: click.Context):
        opts, opt_help = super().get_help_record(ctx)

        group_option_names = list(self.group.get_options(ctx))
        group_option_names.reverse()

        indent_inc = ctx.make_formatter().indent_increment
        indent = ' ' * indent_inc

        if self.name == group_option_names[0]:
            group_name, group_help = self.group.get_help_record(ctx)
            opts = f'\n{indent}{group_name}:\n{indent*2}{opts}'
            opt_help = f'{opt_help}'
        else:
            opts = f'{indent}{opts}'

        return opts, opt_help


class OptionGroup:
    """Option group manages grouped (related) options
    """

    def __init__(self, name: ty.Optional[str] = None, description: ty.Optional[str] = None, *,
                 requied: bool = False) -> None:
        self._name = name if name else ''
        self._description = description if description else ''
        self._requied = requied
        self._options = {}

    @property
    def name(self) -> str:
        """Returns the group name or empty string if it was not set

        :return: group name
        """
        return self._name

    @property
    def description(self) -> str:
        """Returns the group description or empty string if it was not set

        :return: group description
        """
        return self._description

    @property
    def required(self) -> bool:
        """Returns 'required' flag

        If 'required' is True, at least one option from the group must be set.

        :return: required flag
        """
        return self._requied

    def get_default_name(self, ctx: click.Context) -> str:
        """Returns default name for the group

        :param ctx: Click Context object
        :return: group default name
        """
        if self.name:
            return self.name

        option_names = reversed(list(self.get_options(ctx)))
        option_names = '|'.join(option_names)
        return f'({option_names})'

    def get_help_record(self, ctx: click.Context) -> ty.Tuple[str, str]:
        """Returns the help record for the group

        :param ctx: Click Context object
        :return: the tuple of two fileds: (name, description)
        """
        name = self.get_default_name(ctx)
        descr = self.description if self.description else ''

        if self.required:
            name += ' [required]'

        return name, descr

    def option(self, *param_decls, **attrs):
        """Decorator attaches an grouped option to the command
        """
        def decorator(func):
            option_attrs = attrs.copy()
            option_attrs.setdefault('cls', GroupedOption)

            if not issubclass(option_attrs['cls'], GroupedOption):
                raise TypeError("'cls' argument must be a subclass of 'GroupedOption' class.")

            self._check_decorated_order(func)
            func = click.option(*param_decls, group=self, **option_attrs)(func)
            self._option_memo(func)
            return func

        return decorator

    def handle_parse_result(self, option: GroupedOption, ctx: click.Context, opts: dict) -> None:
        if not self.required:
            return
        if option.name in opts:
            return

        options = self.get_options(ctx)

        if not set(options).intersection(opts):
            error_text = f'At least one option from "{self.get_default_name(ctx)}" option group is required:'

            for opt in reversed(list(options.values())):
                error_text += f'\n  {opt.get_error_hint(ctx)}'

            raise click.UsageError(error_text, ctx=ctx)

    def _check_decorated_order(self, func):
        if isinstance(func, click.Command):
            params = func.params
            func = func.callback
        else:
            params = getattr(func, '__click_params__', [])

        if not params or func not in self._options:
            return

        last_param = params[-1]
        options = self._options[func]

        if last_param.name not in options:
            hint_list = last_param.opts or [last_param.human_readable_name]

            raise ValueError((
                "Group's options must not be mixed with "
                "other options while adding by decorator. "
                f"Check decorator position for {hint_list} option."
            ))

    def _option_memo(self, func):
        if isinstance(func, click.Command):
            params = func.params
            func = func.callback
        else:
            params = func.__click_params__

        option: GroupedOption = params[-1]
        self._options.setdefault(func, {})[option.name] = option

    def get_options(self, ctx: click.Context) -> dict:
        return self._options.get(ctx.command.callback, {})


class MutuallyExclusiveOptionGroup(OptionGroup):
    """Option group with mutually exclusive behavior for grouped options
    """

    def get_help_record(self, ctx: click.Context) -> ty.Tuple[str, str]:
        name = self.get_default_name(ctx)
        descr = self.description if self.description else ''

        if self.required:
            name += ' [mutually_exclusive, required]'
        else:
            name += ' [mutually_exclusive]'

        return name, descr

    def handle_parse_result(self, option: GroupedOption, ctx: click.Context, opts: dict) -> None:
        options = self.get_options(ctx)
        given_option_names = set(options).intersection(opts)

        if self.required and not given_option_names:
            error_text = ('One required option must be set from '
                          f'the mutually exclusive option group "{self.get_default_name(ctx)}":')

            for option in reversed(list(options.values())):
                opt_err_hint = option.get_error_hint(ctx)
                error_text += f'\n  {opt_err_hint}'

            raise click.UsageError(error_text, ctx=ctx)

        if len(given_option_names) > 1:
            error_text = f'The given mutually exclusive options cannot be used at the same time:'

            for opt_name in given_option_names:
                opt_err_hint = options[opt_name].get_error_hint(ctx)
                error_text += f'\n  {opt_err_hint}'

            raise click.UsageError(error_text, ctx=ctx)

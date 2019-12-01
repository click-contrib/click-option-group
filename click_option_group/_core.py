# -*- coding: utf-8 -*-

import typing as ty
import random
import string
import weakref

import click
from click.core import augment_usage_errors


_FAKE_OPT_NAME_LEN = 30


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

        fake_option = self.group.get_fake_option(ctx)
        if not fake_option:
            return opts, opt_help

        if self.name == fake_option.name:
            return self.group.get_help_record(ctx)
        else:
            formatter = ctx.make_formatter()
            with formatter.indentation():
                indent = ' ' * formatter.current_indent
                return f'{indent}{opts}', opt_help


class OptionGroup:
    """Option group manages grouped (related) options
    """

    def __init__(self, name: ty.Optional[str] = None, help: ty.Optional[str] = None, *,
                 required: bool = False) -> None:
        self._name = name if name else ''
        self._help = help if help else ''
        self._required = required
        self._options = {}
        self._fake_helper_options = {}

    @property
    def name(self) -> str:
        """Returns the group name or empty string if it was not set

        :return: group name
        """
        return self._name

    @property
    def description(self) -> str:
        """Returns the group help or empty string if it was not set

        :return: group help
        """
        return self._help

    @property
    def required(self) -> bool:
        """Returns 'required' flag

        If 'required' is True, at least one option from the group must be set.

        :return: required flag
        """
        return self._required

    @property
    def name_extra(self) -> ty.List[str]:
        return ['required'] if self.required else []

    def get_default_name(self, ctx: click.Context) -> str:
        """Returns default name for the group

        :param ctx: Click Context object
        :return: group default name
        """
        if self.name:
            return self.name

        option_names = reversed(list(self.get_options(ctx)))
        option_names = '|'.join(option_names)
        return f'{option_names}'

    def get_help_record(self, ctx: click.Context) -> ty.Tuple[str, str]:
        """Returns the help record for the group

        :param ctx: Click Context object
        :return: the tuple of two fileds: (name, help)
        """

        name = self.get_default_name(ctx)
        descr = self.description if self.description else ''

        extra = ', '.join(self.name_extra)
        if extra:
            extra = f'[{extra}]'

        name = f'({name}) GROUP {extra}'

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

            # Add the fake invisible option to use for print nice help for grouped options
            self._add_fake_helper_option(func)

            return func

        return decorator

    def get_options(self, ctx: click.Context) -> dict:
        return self._options.get(ctx.command.callback, {})

    def get_fake_option(self, ctx: click.Context) -> ty.Optional[GroupedOption]:
        return self._fake_helper_options.get(ctx.command.callback)

    def handle_parse_result(self, option: GroupedOption, ctx: click.Context, opts: dict) -> None:
        if not self.required:
            return
        if option.name in opts:
            return

        options = self.get_options(ctx)

        if not set(options).intersection(opts):
            error_text = f'None of the required options are set from "{self.get_default_name(ctx)}" option group:'

            for opt in reversed(list(options.values())):
                error_text += f'\n  {opt.get_error_hint(ctx)}'

            raise click.UsageError(error_text, ctx=ctx)

    @staticmethod
    def _get_callback_and_params(func):
        if isinstance(func, click.Command):
            params = func.params
            func = func.callback
        else:
            params = getattr(func, '__click_params__', [])

        return func, params

    def _check_decorated_order(self, func):
        func, params = self._get_callback_and_params(func)

        if not params or func not in self._options:
            return

        last_param = params[-1]
        fake_option = self._fake_helper_options[func]
        options = self._options[func]

        if last_param.name != fake_option.name and last_param.name not in options:
            hint_list = last_param.opts or [last_param.human_readable_name]

            raise ValueError((
                "Group's options must not be mixed with "
                "other options while adding by decorator. "
                f"Check decorator position for {hint_list} option."
            ))

    def _add_fake_helper_option(self, func):
        callback, params = self._get_callback_and_params(func)

        if callback not in self._fake_helper_options:
            fake_opt_name = ''.join(random.choices(string.ascii_lowercase, k=_FAKE_OPT_NAME_LEN))
            func = click.option(f'--{fake_opt_name}',
                                group=self, cls=GroupedOption, expose_value=False)(func)

            _, params = self._get_callback_and_params(func)
            self._fake_helper_options[callback] = params[-1]

        fake_option = self._fake_helper_options[callback]
        last_option = params[-1]

        if fake_option.name != last_option.name:
            # Hold fake option on the top of the option group
            fake_index = params.index(fake_option)
            params[-1], params[fake_index] = params[fake_index], params[-1]

    def _option_memo(self, func):
        func, params = self._get_callback_and_params(func)

        option: GroupedOption = params[-1]
        self._options.setdefault(func, {})[option.name] = option


class MutuallyExclusiveOptionGroup(OptionGroup):
    """Option group with mutually exclusive behavior for grouped options
    """

    @property
    def name_extra(self) -> ty.List[str]:
        return super().name_extra + ['mutually_exclusive']

    def handle_parse_result(self, option: GroupedOption, ctx: click.Context, opts: dict) -> None:
        super().handle_parse_result(option, ctx, opts)

        options = self.get_options(ctx)
        given_option_names = set(options).intersection(opts)

        if len(given_option_names) > 1:
            error_text = f'The given mutually exclusive options cannot be used at the same time:'

            for opt_name in given_option_names:
                opt_err_hint = options[opt_name].get_error_hint(ctx)
                error_text += f'\n  {opt_err_hint}'

            raise click.UsageError(error_text, ctx=ctx)

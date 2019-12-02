# -*- coding: utf-8 -*-

import typing as ty
import collections.abc as abc
import warnings

import click

from ._core import OptionGroup
from ._helpers import get_callback_and_params, raise_mixing_decorators_error


class StateStackItem(ty.NamedTuple):
    param_decls: ty.Tuple[str, ...]
    attrs: ty.Dict[str, ty.Any]
    params: ty.List[click.Option]


class _OptGroup:
    """A helper class for manage creating groups and group options via decorating
    """

    def __init__(self) -> None:
        self._decorating_state: ty.Dict[abc.Callable, ty.List[StateStackItem]] = {}

    def group(self, name: ty.Optional[str] = None, help: ty.Optional[str] = None,
              cls: ty.Optional[OptionGroup] = None, **attrs):
        """

        :param name:
        :param help:
        :param cls:
        :param attrs:
        :return:
        """
        def decorator(func):
            callback, params = get_callback_and_params(func)

            if callback not in self._decorating_state:
                warnings.warn(
                    'There is attempt to add an empty option group. The group will not be added.',
                    UserWarning)
                return func

            options_stack = self._decorating_state.get(callback, [])
            self._check_mixing_decorators(options_stack, params)

            return func
        return decorator

    def option(self, *param_decls, **attrs):
        """

        :param param_decls:
        :param attrs:
        :return:
        """
        def decorator(func):
            callback, params = get_callback_and_params(func)
            options_stack = self._decorating_state.setdefault(callback, [])

            self._check_mixing_decorators(options_stack, params)
            options_stack.append(StateStackItem(param_decls, attrs, params))

            return func

        return decorator

    @staticmethod
    def _check_mixing_decorators(options_stack, params):
        if options_stack:
            last_state = options_stack[-1]
            if len(params) > len(last_state.params):
                raise_mixing_decorators_error(params[-1])


optgroup = _OptGroup()
"""Decorator creates groups of options and adds options into groups
"""

# -*- coding: utf-8 -*-

import typing as ty
import collections.abc as abc
import random
import string

import click


FAKE_OPT_NAME_LEN = 30


def get_callback_and_params(func) -> ty.Tuple[abc.Callable, ty.List[click.Option]]:
    """Returns callback function and its parameters list

    :param func: decorated function or click Command
    :return: (callback, params)
    """
    if isinstance(func, click.Command):
        params = func.params
        func = func.callback
    else:
        params = getattr(func, '__click_params__', [])

    return func, params


def get_fake_option_name(name_len: int = FAKE_OPT_NAME_LEN):
    return '--' + ''.join(random.choices(string.ascii_lowercase, k=name_len))


def raise_mixing_decorators_error(wrong_option: click.Option):
    hint_list = wrong_option.opts or [wrong_option.name]

    raise ValueError((
        "Group's options must not be mixed with other options while adding by decorator. "
        f"Check decorator position for {hint_list} option."
    ))

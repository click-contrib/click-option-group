# -*- coding: utf-8 -*-
"""
click-option-group
~~~~~~~~~~~~~~~~~~

Option groups missing in Click

:copyright: © 2019 by Eugene Prilepin
:license: BSD, see LICENSE for more details.
"""

from ._version import __version__  # noqa

from ._core import (
    GroupedOption,
    OptionGroup,
    RequiredAnyOptionGroup,
    RequiredAllOptionGroup,
    MutuallyExclusiveOptionGroup
)

from ._decorators import optgroup


__all__ = [
    'optgroup',
    'GroupedOption',
    'OptionGroup',
    'RequiredAnyOptionGroup',
    'RequiredAllOptionGroup',
    'MutuallyExclusiveOptionGroup',
]

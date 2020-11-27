# -*- coding: utf-8 -*-
"""
click-option-group
~~~~~~~~~~~~~~~~~~

Option groups missing in Click

:copyright: © 2019-2020 by Eugene Prilepin
:license: BSD, see LICENSE for more details.
"""

from ._version import __version__

from ._core import (
    GroupedOption,
    OptionGroup,
    RequiredAnyOptionGroup,
    AllOptionGroup,
    RequiredAllOptionGroup,
    MutuallyExclusiveOptionGroup,
    RequiredMutuallyExclusiveOptionGroup,
)

from ._decorators import optgroup


__all__ = [
    '__version__',
    'optgroup',
    'GroupedOption',
    'OptionGroup',
    'RequiredAnyOptionGroup',
    'AllOptionGroup',
    'RequiredAllOptionGroup',
    'MutuallyExclusiveOptionGroup',
    'RequiredMutuallyExclusiveOptionGroup',
]

# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging

from typing import Union

from .type import is_int
from .type import is_str
from .type import is_list


def _set_logging_level(name: Union[str, list], level: Union[int, str, list]) -> None:
    """Private function _set_logging_level() sets the logging level of the given module.

    :Args:
        - name: {Union[str, list]} Name or names.
        - level: {Union[int, str, list]} Level or levels.

    :Returns:
        - {None}
    """
    if is_str(name):
        if not is_str(level) and not is_int(level):
            raise ValueError(
                "_set_logging_level: argument level must either be an str or an int when name is str")
        logging.getLogger(name).setLevel(level)
    elif is_list(name):
        if not is_str(level) and not is_int(level) and not is_list(level):
            raise ValueError(
                "_set_logging_level: argument level must either be an str or an int or a list when name is list")
        elif is_list(level):
            assert len(name) == len(
                level), "_set_logging_level: name list and level list are not equal"
            for name_, level_ in zip(name, level):
                logging.getLogger(name_).setLevel(level_)
        else:
            for name_ in name:
                logging.getLogger(name_) .setLevel(level)


def disable_logging(name: str, level: Union[int, str] = logging.CRITICAL) -> None:
    """Function disable_logging() disables the logging of the given module.

    It disables the logging of the given module by setting the logging level to the highest
    value as possible. It may also get a level value explicitly.

    :Args:
        - name: {str} Module name.
        - level: {Union[int, str]} Level.

    :Returns:
        - {None}
    """
    _set_logging_level(name, level)


def enable_logging(name: str, level: Union[int, str] = logging.DEBUG) -> None:
    """Function enable_logging() enables the logging of the given module.

    It enables the logging of the given module by setting the logging level to the lowest
    value as possible. It may also get a level value explicitly.

    :Args:
        - name: {str} Module name.
        - level: {Union[int, str]} Level.

    :Returns:
        - {None}
    """
    _set_logging_level(name, level)

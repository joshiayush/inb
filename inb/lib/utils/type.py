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

# from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!
from __future__ import annotations

from typing import Any


def _type(t: Any) -> str:
  """Function _type() returns the class name of the object given.

  :Args:
      - t: {Any} Object we need to find the class name for.

  :Returns:
      - {str} Class name if __name__ attribute is present otherwise None.
  """
  try:
    return t.__name__
  except AttributeError:
    return None


"""Function is_int() returns True if the instance given is an int.

:Args:
    - field: {Any} Instance.

:Returns:
    - {bool} True if the instance is an int otherwise False.
"""
is_int: function = lambda field: isinstance(field, int)

"""Function is_str() returns True if the instance given is an str.

:Args:
    - field: {Any} Instance.

:Returns:
    - {bool} True if the instance is an str otherwise False.
"""
is_str: function = lambda field: isinstance(field, str)

"""Function is_list() returns True if the instance given is an list.

:Args:
    - field: {Any} Instance.

:Returns:
    - {bool} True if the instance is an list otherwise False.
"""
is_list: function = lambda field: isinstance(field, list)

"""Function is_none() returns True if the instance given is None.

:Args:
    - field: {Any} Instance.

:Returns:
    - {bool} True if the instance is None otherwise False.
"""
is_none: function = lambda field: field is None


def is_empty(field: str) -> bool:
  """Function is_empty() returns True if the instance given is empty.

  :Args:
      - field: {str} Instance.

  :Returns:
      - {bool} True if the given instance is empty otherwise False.
  """
  if is_str(field):
    return field.strip() == ''
  return False


def is_present(obj: Any, field: Any) -> bool:
  """Function is_present() returns True if the instance given contains the obj.

  :Args:
      - field: {Any} Instance.
      - obj: {Any} Instance to find.

  :Returns:
      - {bool} True if the instance given contains obj otherwise False.
  """
  if not is_int(field):
    return obj in field
  return False

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

from __future__ import annotations

from typing import (Any, Dict, List)

import os
import stat
import warnings
import functools


def Type(t: Any) -> str:
  try:
    return t.__name__
  except AttributeError:
    return None


def Which(program):

  def is_exe(fpath):  # pylint: disable=invalid-name
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

  fpath, _ = os.path.split(program)
  if fpath:
    if is_exe(program):
      return program
  else:
    for path in os.environ['PATH'].split(os.pathsep):
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file

  return None


def IgnoreWarnings(type_: Warning):

  def decorater(func: function):  # pylint: disable=undefined-variable, invalid-name

    @functools.wraps(func)
    def wrapper(self, *args: List[Any], **kwargs: Dict[Any, Any]):  # pylint: disable=invalid-name
      with warnings.catch_warnings():
        warnings.simplefilter('ignore', type_)
        func(self, *args, **kwargs)

    return wrapper

  return decorater


def RemoveFilePermissions(path: str, bit: str):
  assert bit in (
      'r', 'w',
      'x'), "Expected either of ('r', 'w', 'x'), received %(bit)s." % {
          'bit': bit
      }
  if bit == 'r':
    new_bit_mask = ~stat.S_IRUSR & ~stat.S_IRGRP & ~stat.S_IROTH
  elif bit == 'w':
    new_bit_mask = ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
  elif bit == 'x':
    new_bit_mask = ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH
  os.chmod(path, stat.S_IMODE(os.lstat(path).st_mode) & new_bit_mask)


def AddFilePermissions(path: str, bit: str):
  assert bit in (
      'r', 'w',
      'x'), "Expected either of ('r', 'w', 'x'), received %(bit)s." % {
          'bit': bit
      }
  if bit == 'r':
    new_bit_mask = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
  elif bit == 'w':
    new_bit_mask = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
  elif bit == 'x':
    new_bit_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
  os.chmod(path, stat.S_IMODE(os.lstat(path).st_mode) | new_bit_mask)

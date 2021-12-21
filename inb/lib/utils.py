# Copyright 2021, joshiayus Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of joshiayus Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

from typing import (Any, Dict, List)

import os
import stat
import warnings
import functools


def Type(t: Any) -> str:
  """Returns the name of the type used.

  This function is different from the built-in type which returns
  `<class 'type'>` for primitive and user-defined types not the actual name
  of that type; this function does that for us.

  ```python
  >>> print(Type(int))
  'int'
  >>> print(Type(None))
  None
  ```

  Args:
    t: Any type.

  Returns:
    Type name.
  """
  try:
    return t.__name__
  except AttributeError:
    return None


def Which(program: str) -> str:
  """Returns the executable for the program name given.

  This function searches for the executable for the program name given either
  in the system's environment `PATH` or in the program name itself which could
  be a filesystem path.

  Note: In order to get a executable returned from this function by the program
  name given not only the executable needs to be present in the `PATH` or
  `program path` but it also must have its x-bit turned on.

  ```python
  >>> Which('python')
  '/usr/bin/python'
  ```

  Args:
    program: Program name or path to program.

  Returns:
    Program name if present and executable in the environment `PATH` or the
      `program path` given.
    None if the above does not satisfy.
  """

  def is_exe(fpath: str):  # pylint: disable=invalid-name
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


def IgnoreWarnings(type_: Warning) -> function:  # pylint: disable=undefined-variable
  """Wrapper around your function that generates any kind of `Warnings`.

  This function is a wrapper that ignores any kind of warning specified.  You
  usually use this function to decorate functions that generates any kind of
  warnings and you don't want them.  This function catches such warnings and
  ignores them.

  ```python
  @IgnoreWarnings(ResourceWarning)
  def foo(*args, **kwargs) -> None:
    warnings.warn('I'm gonna generate a ResourceWarning for no reason',
                  ResourceWarning)
  ```

  Args:
    type_: Warning type.  It could be among the following subclasses of
            `Warning`,

  ```python
  [ UserWarning, DeprecationWarning, SyntaxWarning,
    RuntimeWarning, FutureWarning, PendingDeprecationWarning,
    ImportWarning, UnicodeWarning, BytesWarning, ResourceWarning, ]
  ```

  Returns:
    Ignore warnings wrapper around the given function.
  """

  def decorater(func: function) -> function:  # pylint: disable=undefined-variable, invalid-name

    @functools.wraps(func)
    def wrapper(*args: List[Any], **kwargs: Dict[Any, Any]) -> None:  # pylint: disable=invalid-name
      with warnings.catch_warnings():
        warnings.simplefilter('ignore', type_)
        func(*args, **kwargs)

    return wrapper

  return decorater


def RemoveFilePermissions(path: str, bit: str) -> None:
  """As name suggests this function removes file permissions from the given
  file.

  This function removes permissions from a file by turning the given file bit
  off for all the categories i.e., user, group and other.

  Note: This function should be only called when the process is ran as root
  otherwise you will receive `Permission Denied` exception from the `os` module.

  ```python
  RemoveFilePermissions('myfile', 'x')  # turns the x-bit off
  ```

  Args:
    path: File path.
    bit: File bit to turn off, could be one of the following,

  ```python
  ('r', 'w', 'x')
  ```
  """
  assert bit in ('r', 'w',
                 'x'), f"Expected either of ('r', 'w', 'x'), received {bit}."
  if bit == 'r':
    new_bit_mask = ~stat.S_IRUSR & ~stat.S_IRGRP & ~stat.S_IROTH
  elif bit == 'w':
    new_bit_mask = ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
  elif bit == 'x':
    new_bit_mask = ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH
  os.chmod(path, stat.S_IMODE(os.lstat(path).st_mode) & new_bit_mask)


def AddFilePermissions(path: str, bit: str):
  """As name suggests this function adds file permissions to the given file.

  This function adds permissions to a file by turning the given file bit on for
  all the categories i.e., user, group and other.

  Note: This function should be only called when the process is ran as root
  otherwise you will receive `Permission Denied` exception from the `os` module.

  ```python
  AddFilePermissions('myfile', 'x')  # turns the x-bit on
  ```

  Args:
    path: File path.
    bit: File bit to turn on, could be one of the following,

  ```python
  ('r', 'w', 'x')
  ```
  """
  assert bit in ('r', 'w',
                 'x'), f"Expected either of ('r', 'w', 'x'), received {bit}."
  if bit == 'r':
    new_bit_mask = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
  elif bit == 'w':
    new_bit_mask = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH
  elif bit == 'x':
    new_bit_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
  os.chmod(path, stat.S_IMODE(os.lstat(path).st_mode) | new_bit_mask)

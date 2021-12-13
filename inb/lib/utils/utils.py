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

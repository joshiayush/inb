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

import re
import os
import sys
import errno

from lib.utils.type import (
    is_str,
    is_none,
    is_empty,
)


class Validator(object):
  # Windows-specific error code indicating an invalid pathname.
  # Sadly, Python fails to provide the following magic number for us.
  ERROR_INVALID_NAME = 123

  def __init__(self: Validator, field: str) -> None:
    """Constructor method initializes the field attribute. It also checks if the field
    given is an instance of string or not.

    :Args:
        - self: {Validator} self.
        - field: {str} Field to validate.

    :Returns:
        - {None}

    :Raises:
        - {ValueError} If the field is not an string instance.
    """
    if is_str(field):
      self._field = field
    else:
      raise ValueError(
          "Value %(field)s is not a valid value for Validator instance!" % {"field": field})

  def is_url(self: Validator) -> bool:
    """Method is_url() checks if the field given is a valid url or not using regex.

    :Args:
        - self: {Validator} self.

    :Returns:
        - {bool} True if the field is valid, otherwise False.
    """
    _regex = re.compile(
        r"^(?:http|ftp)s?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$", re.IGNORECASE)
    return re.match(_regex, self._field) is not None

  def is_email(self: Validator) -> bool:
    """Method is_email() checks if the field given is a valid email or not using regex.

    :Args:
        - self: {Validator} self.

    :Returns:
        - {bool} True if the field is valid, otherwise False.
    """
    _regex = re.compile(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.IGNORECASE)
    return re.match(_regex, self._field) is not None

  def is_path(self: Validator) -> bool:
    """Method is_path() checks if the field given is a valid file system path or not.

    :Args:
        - self: {Validator} self.

    :Returns:
        - {bool} True if the field is valid, otherwise False.
    """
    # If this pathname is either not a string or is but is empty, this pathname
    # is invalid.
    try:
      if is_none(
              self._field) or not is_str(
              self._field) or is_empty(
              self._field):
        return False

      # Strip this pathname's Windows-specific drive specifier (e.g., `C:\`)
      # if any. Since Windows prohibits path components from containing `:`
      # characters, failing to strip this `:`-suffixed prefix would
      # erroneously invalidate all valid absolute Windows pathnames.
      _, self._field = os.path.splitdrive(self._field)

      # Directory guaranteed to exist. If the current OS is Windows, this is
      # the drive to which Windows was installed (e.g., the "%HOMEDRIVE%"
      # environment variable); else, the typical root directory.
      if sys.platform == "win32":
        root_dirname = os.environ.get("HOMEDRIVE", "C:")
      else:
        root_dirname = os.path.sep

      # ...Murphy and her ironclad Law
      assert os.path.isdir(root_dirname)

      # Append a path separator to this directory if needed.
      root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

      # Test whether each path component split from this pathname is valid or
      # not, ignoring non-existent and non-readable path components.
      for pathname_part in self._field.split(os.path.sep):
        try:
          os.lstat(root_dirname + pathname_part)
        except OSError as exc:
          # If an OS-specific exception is raised, its error code indicates
          # whether this pathname is valid or not. Unless this is the case,
          # this exception implies an ignorable kernel or filesystem complaint
          # (e.g., path not found or inaccessible).
          #
          # Only the following exceptions indicate invalid pathnames:
          #
          # * Instances of the Windows-specific "WindowsError" class defining the
          #   "winerror" attribute whose value is "ERROR_INVALID_NAME".
          #   Under Windows, "winerror" is more fine-grained and hence useful than
          #   the generic "errno" attribute. When a too-long pathname is passed,
          #   for example, "errno" is "ENOENT" (i.e., no such file or directory)
          #   rather than "ENAMETOOLONG" (i.e., file name too long).
          # * Instances of the cross-platform "OSError" class defining the generic
          #   "errno" attribute whose value is either:
          #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
          #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
          if hasattr(exc, "winerror"):
            if exc.winerror == Validator.ERROR_INVALID_NAME:
              return False
          elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
            return False
    except TypeError as exc:
      # If a "TypeError" exception was raised, it almost certainly has the
      # error message "embedded NUL character" indicating an invalid pathname.
      return False
    # If no exception was raised, all path components and hence this pathname itself
    # are valid. (Praise be to the curmudgeonly python.)
    else:
      return True
    # If any other exception was raised, this is an unrelated fatal issue
    # (e.g., a bug). Permit this exception to unwind the call stack.

  def is_executable(self: Validator) -> bool:
    """Method is_executable() checks if the executable bit of a path is on or not.

    :Args:
        - self: {Validator} self.

    :Returns:
        - {bool} True if the executable bit is on, False otherwise.
    """
    def is_exe(fpath: str) -> bool:
      """Function is_exe() checks if the given path is valid and executable.

      :Args:
          - fpath: {str} File path.

      :Returns:
          - {bool} True if the file path is valid and executable, False otherwise.
      """
      return self.is_path() and os.access(
          fpath, os.X_OK)  # check if the x bit is OK

    # split the path in a tuple containing (head, tail)
    fpath, _ = os.path.split(self._field)
    if fpath:
      # if we successfully obtained a head, check if the given field
      # is a path
      if is_exe(self._field):
        return True
    else:
      # if we didn't obtain a head then we want to seek into the system's
      # binary path for the executable
      sys_bin_path = os.environ["PATH"].split(os.pathsep)
      for path in sys_bin_path:
        # join the executable with the system environment path and check
        # if the x bit is OK
        exe_file = os.path.join(path, self._field)
        if is_exe(exe_file):
          return True
    return False


class InbValidator(object):
  def __init__(self: InbValidator, field: str) -> None:
    """Constructor method initializes the field attribute. It also checks if the field
    given is an instance of string or not.

    This constructor method also creates an instance of the Validator class to use for
    validating emails and urls.

    :Args:
        - self: {Validator} self.
        - field: {str} Field to validate.

    :Returns:
        - {None}

    :Raises:
        - {ValueError} If the field is not an string instance.
    """
    if is_str(field):
      self._field = field
    else:
      raise ValueError(
          "Value %(field)s is not a valid value for Validator instance!" % {"field": field})
    self.__validator = Validator(self._field)

  def is_url(self: InbValidator) -> bool:
    """Method is_url() checks if the given field is a LinkedIn url or not.

    This method takes help of the Validator::is_url() method to validate the url once
    it is confirmed that this url connects us with the LinkedIn server.

    :Args:
        - self: {InbValidator} self.

    :Returns:
        - {bool} True if the url is valid, False otherwise.
    """
    base_url = ["http://www.linkedin.com", "https://www.linkedin.com"]
    for url in base_url:
      if self._field.startswith(url):
        if self.__validator.is_url():
          return True
    return False

  def is_email(self: InbValidator) -> bool:
    """Method is_email() checks if the field given is a valid email or not using regex.

    :Args:
        - self: {InbValidator} self.

    :Returns:
        - {bool} True if the field is valid, otherwise False.
    """
    return self.__validator.is_email()

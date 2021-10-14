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

import os
import stat
import unittest

from lib import DRIVER_PATH
from lib.utils.validator import Validator


class TestValidatorClass(unittest.TestCase):

  def test_validator_error_code(self: TestValidatorClass) -> None:
    self.assertEqual(Validator.ERROR_INVALID_NAME, 123)

  def test_validator_constructor_exception(
          self: TestValidatorClass) -> None:
    different_types = [10, 10.19, [1, 2, 3, 4],
                       ["abc", "bcd", "cdb"], {"name": "ayush"}]
    for i in range(len(different_types)):
      with self.assertRaises(ValueError):
        Validator(different_types[i])

  def test_validator_constructor(self: TestValidatorClass) -> None:
    validator = Validator("https://www.linkedin.com/")
    self.assertEqual(validator._field, "https://www.linkedin.com/")

  def test_validator_is_url_method(self: TestValidatorClass) -> None:
    self.assertTrue(Validator("http://www.linkedin.com/").is_url())
    self.assertTrue(Validator("https://www.linkedin.com/").is_url())
    self.assertTrue(Validator("ftp://www.linkedin.com/").is_url())
    self.assertTrue(Validator("ftps://www.linkedin.com/").is_url())
    self.assertTrue(Validator(
        "https://www.linkedin.com/in/ornela-cerenishti-118400146/").is_url())
    self.assertFalse(Validator("notavalidurl").is_url())
    self.assertFalse(
        Validator("/ornela-cerenishti-118400146/").is_url())

  def test_validator_is_email_method(
          self: TestValidatorClass) -> None:
    self.assertTrue(Validator("ayush854032@gmail.com").is_email())
    self.assertTrue(
        Validator("joshiayush.joshiayush@gmail.com").is_email())
    self.assertTrue(
        Validator("joshiayush.joshiayush@yahoo.com").is_email())
    self.assertTrue(
        Validator("joshiayush.joshiayush@apple.com").is_email())
    self.assertTrue(
        Validator("joshiayush.joshiayush@joshiayush.com").is_email())
    self.assertTrue(
        Validator("joshiayush.joshiayush@microsoft.com").is_email())
    self.assertTrue(
        Validator("joshiayush.joshiayush@google.com").is_email())
    self.assertFalse(Validator("@gmail.com").is_email())
    self.assertFalse(Validator(".com@gmail").is_email())

  def test_validator_is_path_method(self: TestValidatorClass) -> None:
    self.assertTrue(Validator(os.path.abspath(__file__)).is_path())

  @unittest.skipIf(not os.getuid() == 0,
                   "Cannot alter permissions without root!")
  def test_validator_is_executable_method(
          self: TestValidatorClass) -> None:
    original_file_permissions = stat.S_IMODE(
        os.lstat(DRIVER_PATH).st_mode)

    def add_execute_permissions(path):
      """Add write permissions from this path, while keeping all other 
      permissions intact.

      Params:
          path:  The path whose permissions to alter.
      """
      ADD_USER_EXECUTE = stat.S_IXUSR
      ADD_GROUP_EXECUTE = stat.S_IXGRP
      ADD_OTHER_EXECUTE = stat.S_IXOTH
      ADD_EXECUTE = ADD_USER_EXECUTE | ADD_GROUP_EXECUTE | ADD_OTHER_EXECUTE

      current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
      os.chmod(path, current_permissions | ADD_EXECUTE)

    add_execute_permissions(DRIVER_PATH)
    self.assertTrue(Validator(DRIVER_PATH).is_executable())

    def remove_execute_permissions(path):
      """Remove write permissions from this path, while keeping all other 
      permissions intact.

      Params:
          path:  The path whose permissions to alter.
      """
      NO_USER_EXECUTE = ~stat.S_IXUSR
      NO_GROUP_EXECUTE = ~stat.S_IXGRP
      NO_OTHER_EXECUTE = ~stat.S_IXOTH
      NO_EXECUTE = NO_USER_EXECUTE & NO_GROUP_EXECUTE & NO_OTHER_EXECUTE

      current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
      os.chmod(path, current_permissions & NO_EXECUTE)

    remove_execute_permissions(DRIVER_PATH)
    self.assertFalse(Validator(DRIVER_PATH).is_executable())

    # place the original file permissions back
    os.chmod(DRIVER_PATH, original_file_permissions)

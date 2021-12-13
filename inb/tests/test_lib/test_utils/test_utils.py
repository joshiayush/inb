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

import os
import sys
import stat
import unittest
import warnings

from unittest import mock

from lib import utils
from linkedin import settings


class TestCustomTypeUtilityFunction(unittest.TestCase):

  def test_with_primitive_types(self) -> None:
    types_ = [
        (int, 'int'),
        (str, 'str'),
        (float, 'float'),
        (set, 'set'),
        (list, 'list'),
        (dict, 'dict'),
        (None, None),
    ]
    for type_ in types_:
      self.assertEqual(utils.Type(type_[0]), type_[1])

  def test_with_custom_types(self) -> None:
    types_ = [
        (TestCustomTypeUtilityFunction, 'TestCustomTypeUtilityFunction'),
    ]
    for type_ in types_:
      self.assertEqual(utils.Type(type_[0]), type_[1])


class TestWhichUtilityFunction(unittest.TestCase):

  def test_with_python_executable(self) -> None:
    self.assertEqual(utils.Which(sys.executable), sys.executable)


class TestIgnoreWarningsUtilityFunction(unittest.TestCase):

  @mock.patch('warnings.simplefilter')
  @mock.patch('warnings.catch_warnings')
  def test_with_subclass_of_builtin_warning(
      self, mock_catch_warnings: mock.Mock,
      mock_simplefilter: mock.Mock) -> None:
    warnings_ = [
        UserWarning,
        DeprecationWarning,
        SyntaxWarning,
        RuntimeWarning,
        FutureWarning,
        PendingDeprecationWarning,
        ImportWarning,
        UnicodeWarning,
        BytesWarning,
        ResourceWarning,
    ]
    with warnings.catch_warnings():
      warnings.simplefilter('ignore', ResourceWarning)
      for warning in warnings_:

        @utils.IgnoreWarnings(warning)  # pylint: disable=cell-var-from-loop
        def func() -> None:
          pass

        func()
        mock_catch_warnings.assert_called()
        mock_simplefilter.assert_called_with('ignore', warning)


@unittest.skipIf(
    not os.getuid() == 0,
    ('\nThis test case requires to be ran as root!\n'
     'You need to run this test suite separately using,\n'
     'python3 inb/test.py TestRemoveFilePermissionsFunction.test_name\n'))
class TestRemoveFilePermissionsAndAddFilePermissionsFunction(unittest.TestCase):
  """Note: This test case is not registered in the main test.py file because it
  needs root permissions to run and when given root the selenium API breaks so
  this test should be ran over command line as root using,

  ```shell
  python3 inb/test.py TestRemoveFilePermissionsAndAddFilePermissionsFunction[.test_name]
  ```
  """

  def test_if_r_bit_is_removed_and_added(self) -> None:
    utils.RemoveFilePermissions(settings.CHROME_DRIVER_ABS_PATH, 'r')
    self.assertTrue(
        bool(
            os.stat(settings.CHROME_DRIVER_ABS_PATH).st_mode & ~stat.S_IRUSR &
            ~stat.S_IRGRP & ~stat.S_IROTH))
    utils.AddFilePermissions(settings.CHROME_DRIVER_ABS_PATH, 'r')
    self.assertTrue(
        bool(
            os.stat(settings.CHROME_DRIVER_ABS_PATH).st_mode | stat.S_IRUSR |
            stat.S_IRGRP | stat.S_IROTH))

  def test_if_w_bit_is_removed_and_added(self) -> None:
    utils.RemoveFilePermissions(settings.CHROME_DRIVER_ABS_PATH, 'w')
    self.assertTrue(
        bool(
            os.stat(settings.CHROME_DRIVER_ABS_PATH).st_mode & ~stat.S_IWUSR &
            ~stat.S_IWGRP & ~stat.S_IWOTH))
    utils.AddFilePermissions(settings.CHROME_DRIVER_ABS_PATH, 'w')
    self.assertTrue(
        bool(
            os.stat(settings.CHROME_DRIVER_ABS_PATH).st_mode | stat.S_IWUSR |
            stat.S_IWGRP | stat.S_IWOTH))

  def test_if_x_bit_is_removed_and_added(self) -> None:
    utils.RemoveFilePermissions(settings.CHROME_DRIVER_ABS_PATH, 'x')
    self.assertTrue(
        bool(
            os.stat(settings.CHROME_DRIVER_ABS_PATH).st_mode & ~stat.S_IXUSR &
            ~stat.S_IXGRP & ~stat.S_IXOTH))
    utils.AddFilePermissions(settings.CHROME_DRIVER_ABS_PATH, 'x')
    self.assertTrue(
        bool(
            os.stat(settings.CHROME_DRIVER_ABS_PATH).st_mode | stat.S_IXUSR |
            stat.S_IXGRP | stat.S_IXOTH))

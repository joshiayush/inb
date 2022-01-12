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

import os
import sys
import stat
import unittest
import warnings

from unittest import mock

import lib
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
      self.assertEqual(lib.Type(type_[0]), type_[1])

  def test_with_custom_types(self) -> None:
    types_ = [
        (TestCustomTypeUtilityFunction, 'TestCustomTypeUtilityFunction'),
    ]
    for type_ in types_:
      self.assertEqual(lib.Type(type_[0]), type_[1])


class TestWhichUtilityFunction(unittest.TestCase):

  def test_with_python_executable(self) -> None:
    self.assertEqual(lib.Which(sys.executable), sys.executable)


class TestIgnoreWarningsUtilityFunction(unittest.TestCase):

  @lib.IgnoreWarnings(ResourceWarning)
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

        @lib.IgnoreWarnings(warning)  # pylint: disable=cell-var-from-loop
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
    lib.RemoveFilePermissions(settings.ChromeDriverAbsolutePath(), 'r')
    self.assertTrue(
        bool(
            os.stat(settings.ChromeDriverAbsolutePath()).st_mode &
            ~stat.S_IRUSR & ~stat.S_IRGRP & ~stat.S_IROTH))
    lib.AddFilePermissions(settings.ChromeDriverAbsolutePath(), 'r')
    self.assertTrue(
        bool(
            os.stat(settings.ChromeDriverAbsolutePath()).st_mode |
            stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH))

  def test_if_w_bit_is_removed_and_added(self) -> None:
    lib.RemoveFilePermissions(settings.ChromeDriverAbsolutePath(), 'w')
    self.assertTrue(
        bool(
            os.stat(settings.ChromeDriverAbsolutePath()).st_mode &
            ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH))
    lib.AddFilePermissions(settings.ChromeDriverAbsolutePath(), 'w')
    self.assertTrue(
        bool(
            os.stat(settings.ChromeDriverAbsolutePath()).st_mode |
            stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))

  def test_if_x_bit_is_removed_and_added(self) -> None:
    lib.RemoveFilePermissions(settings.ChromeDriverAbsolutePath(), 'x')
    self.assertTrue(
        bool(
            os.stat(settings.ChromeDriverAbsolutePath()).st_mode &
            ~stat.S_IXUSR & ~stat.S_IXGRP & ~stat.S_IXOTH))
    lib.AddFilePermissions(settings.ChromeDriverAbsolutePath(), 'x')
    self.assertTrue(
        bool(
            os.stat(settings.ChromeDriverAbsolutePath()).st_mode |
            stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))

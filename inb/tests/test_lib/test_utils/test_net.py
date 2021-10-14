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

from typing import List

import unittest
import platform
import subprocess

from unittest.mock import Mock
from unittest.mock import patch

from lib import ping


@unittest.skipUnless(ping("google.com"),
                     "Domain Name System Not Resolved")
class TestPingFunction(unittest.TestCase):

  @patch("subprocess.call")
  def test_ping_method_with_valid_host(
          self: TestPingFunction, mock_subproc_call: Mock) -> None:
    host = "google.com"
    self.assertTrue(ping(host))
    if platform.system().lower() == "windows":
      param = "-n"
    else:
      param = "-c"
    command: List[str] = ["ping", param, '1', host]
    mock_subproc_call.assert_called_with(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

  @patch("subprocess.call")
  def test_ping_method_with_malformed_host(
          self: TestPingFunction, mock_subproc_call: Mock) -> None:
    host = "name@yahoo.com"
    self.assertFalse(ping(host))
    if platform.system().lower() == "windows":
      param = "-n"
    else:
      param = "-c"
    command: List[str] = ["ping", param, '1', host]
    mock_subproc_call.assert_called_with(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

import unittest

from unittest.mock import Mock
from unittest.mock import patch

from lib import Terminal


class TestTerminalClass(unittest.TestCase):

    def setUp(self: TestTerminalClass) -> None:
        self.t = Terminal()

    @patch("sys.stdout.write")
    def test_setcursorposition_method_with_valid_x_and_y(self: TestTerminalClass, mock_stdout_write: Mock) -> None:
        self.t.setcursorposition(10, 10)
        mock_stdout_write.assert_called_with("%c[%d;%df" % (0x1B, 10, 10))

    def test_getcursorposition_method(self: TestTerminalClass) -> None:
        (x, y) = self.t.getcursorposition()
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)

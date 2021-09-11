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

from lib.utils.figlet import CreateFigletString


class TestCreateFigletFunction(unittest.TestCase):

    @patch("pyfiglet.figlet_format")
    def test_createfigletstring_function_with_one_parameter(
            self: TestCreateFigletFunction,
            mock_figlet_format: Mock
    ) -> None:
        kwargs = {}
        CreateFigletString("inb")
        mock_figlet_format.assert_called_with(
            text="inb", font="standard", **kwargs)

    @patch("pyfiglet.figlet_format")
    def test_createfigletstring_function_with_two_parameters(
            self: TestCreateFigletFunction,
            mock_figlet_format: Mock
    ) -> None:
        kwargs = {}
        CreateFigletString("inb", font="slant")
        mock_figlet_format.assert_called_with(
            text="inb", font="slant", **kwargs)

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

from lib.utils.type import _type


class TestCustomTypeFunction(unittest.TestCase):
    def test_if_output_is_str(self: TestCustomTypeFunction) -> None:
        self.assertIsInstance(_type(int), str)
    
    def test_if_output_is_none(self: TestCustomTypeFunction) -> None:
        self.assertEqual(_type(None), None)

    def test_if_ouput_is_correct(self: TestCustomTypeFunction) -> None:
        self.assertEqual(_type(int), "int")
        self.assertEqual(_type(str), "str")
        self.assertEqual(_type(float), "float")
        self.assertEqual(_type(set), "set")
        self.assertEqual(_type(list), "list")
        self.assertEqual(_type(dict), "dict")
        self.assertEqual(_type(None), None)
        self.assertEqual(_type(TestCustomTypeFunction), "TestCustomTypeFunction")

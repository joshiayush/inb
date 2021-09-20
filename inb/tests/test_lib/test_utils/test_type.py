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
from lib.utils.type import is_int
from lib.utils.type import is_str
from lib.utils.type import is_list
from lib.utils.type import is_none
from lib.utils.type import is_empty
from lib.utils.type import is_present


class TestCustomTypeFunction(unittest.TestCase):
    def test_type_function_if_output_is_str(self: TestCustomTypeFunction) -> None:
        self.assertIsInstance(_type(int), str)

    def test_type_function_if_output_is_none(self: TestCustomTypeFunction) -> None:
        self.assertEqual(_type(None), None)

    def test_type_function_if_ouput_is_correct(self: TestCustomTypeFunction) -> None:
        types_ = [(int, "int"), (str, "str"), (float, "float"), (set, "set"), (list, "list"),
                  (dict, "dict"), (None, None), (TestCustomTypeFunction, "TestCustomTypeFunction")]
        for i in range(len(types_)):
            self.assertEqual(_type(types_[i][0]), types_[i][1])

    def test_is_int_function(self: TestCustomTypeFunction) -> None:
        self.assertTrue(is_int(1), "ERR: function is_int(1) != True")
        invalid_types = ["str", (1, 2, 3, 4), [1, 2, 3, 4], {1: "a", 2: "3"}]
        for type_ in invalid_types:
            self.assertFalse(
                is_int(type_), "ERR: function is_int(%(type_)s) != False" % {"type_": type_})

    def test_is_str_function(self: TestCustomTypeFunction) -> None:
        self.assertTrue(is_str("str"), "ERR: function is_str('str') != True")
        invalid_types = [1, (1, 2, 3, 4), [1, 2, 3, 4], {1: "a", 2: "3"}]
        for type_ in invalid_types:
            self.assertFalse(
                is_str(type_), "ERR: function is_int(%(type_)s) != False" % {"type_": type_})

    def test_is_list_function(self: TestCustomTypeFunction) -> None:
        self.assertTrue(is_list([1]), "ERR: function is_list([1]) != True")
        invalid_types = ["str", (1, 2, 3, 4), 1, {1: "a", 2: "3"}]
        for type_ in invalid_types:
            self.assertFalse(
                is_list(type_), "ERR: function is_int(%(type_)s) != False" % {"type_": type_})

    def test_is_none_function(self: TestCustomTypeFunction) -> None:
        self.assertTrue(is_none(None), "ERR: function is_none(None) != True")
        invalid_types = [1, "str", (1, 2, 3, 4), [1, 2, 3, 4], {
            1: "a", 2: "3"}]
        for type_ in invalid_types:
            self.assertFalse(
                is_none(type_), "ERR: function is_int(%(type_)s) != False" % {"type_": type_})

    def test_is_empty_function(self: TestCustomTypeFunction) -> None:
        self.assertTrue(is_empty("   "),
                        "ERR: function is_empty('   ') != True")
        self.assertFalse(
            is_empty("str"), "ERR: function is_empty('str') != False")

    def test_is_present_function(self: TestCustomTypeFunction) -> None:
        self.assertTrue(is_present(':', "h:h:s"),
                        "ERR: function is_present(':', 'h:h:s') != True")
        self.assertFalse(is_present("str", "ayush"),
                         "ERR: function is_present('str', 'ayush') != False")

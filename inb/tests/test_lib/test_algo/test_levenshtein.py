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

from lib import levenshtein


class TestLevenshteinFunction(unittest.TestCase):

    def test_levenshtein_function_with_invalid_argument_type(self: TestLevenshteinFunction):
        invalid_types = [(1, 1), ([1, 2, 3], [1, 2, 3]), ({
            "levenshtein": "distance"}, {"levenshtein": "distance"})]
        for type_ in invalid_types:
            with self.assertRaises(TypeError):
                levenshtein(*type_)

    def test_levenshtein_function_with_indentical_strings(self: TestLevenshteinFunction):
        str1 = "test_levenshtein_function_with_indentical_strings"
        str2 = "test_levenshtein_function_with_indentical_strings"
        self.assertEqual(levenshtein(
            str1, str2), 0, "ERR: Levenshtein distance does not equal to 0 for string %(s1)s and %(s2)s" %
            {"s1": str1, "s2": str2})

    def test_levenshtein_function_with_strings_with_minimum_edit_distance_of_3(self: TestLevenshteinFunction):
        str2 = "kitten"
        str1 = "sitting"
        self.assertEqual(levenshtein(
            str1, str2), 3, "ERR: Levenshtein distance does not equal to 3 for string %(s1)s and %(s2)s" %
            {"s1": str1, "s2": str2})

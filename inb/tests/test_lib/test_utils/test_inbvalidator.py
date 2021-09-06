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

from lib import Validator
from lib import InbValidator


class TestInbValidatorClass(unittest.TestCase):

    def test_inbvalidator_constructor_method(self: TestInbValidatorClass) -> None:
        validator = InbValidator("https://www.linkedin.com/")
        self.assertEqual(validator._field, "https://www.linkedin.com/")
        # check for the private instance that we make inside of the InbValidator
        # constructor to use for validating the emails and urls given
        self.assertIsInstance(validator._InbValidator__validator, Validator)

    def test_inbvalidator_constructor_method_exception(self: TestInbValidatorClass) -> None:
        different_types = [10, 10.19, [1, 2, 3, 4],
                           ["abc", "bcd", "cdb"], {"name": "ayush"}]
        for _type in different_types:
            with self.assertRaises(ValueError):
                InbValidator(_type)

    def test_inbvalidator_is_url_method(self: TestInbValidatorClass) -> None:
        self.assertTrue(InbValidator("http://www.linkedin.com/").is_url())
        self.assertTrue(InbValidator("https://www.linkedin.com/").is_url())
        self.assertTrue(
            InbValidator("https://www.linkedin.com/in/ornela-cerenishti-118400146/").is_url())
        self.assertFalse(InbValidator("https://www.google.com").is_url())
        self.assertFalse(InbValidator("ftp://www.linkedin.com/").is_url())
        self.assertFalse(InbValidator("ftps://www.linkedin.com/").is_url())
        self.assertFalse(InbValidator("notavalidurl").is_url())
        self.assertFalse(InbValidator(
            "/ornela-cerenishti-118400146/").is_url())

    def test_inbvalidator_is_email_method(self: TestInbValidatorClass) -> None:
        self.assertTrue(InbValidator("ayush854032@gmail.com").is_email())
        self.assertTrue(
            InbValidator("joshiayush.joshiayush@gmail.com").is_email())
        self.assertTrue(
            InbValidator("joshiayush.joshiayush@yahoo.com").is_email())
        self.assertTrue(
            InbValidator("joshiayush.joshiayush@apple.com").is_email())
        self.assertTrue(
            InbValidator("joshiayush.joshiayush@joshiayush.com").is_email())
        self.assertTrue(
            InbValidator("joshiayush.joshiayush@microsoft.com").is_email())
        self.assertTrue(
            InbValidator("joshiayush.joshiayush@google.com").is_email())
        self.assertFalse(InbValidator("@gmail.com").is_email())
        self.assertFalse(InbValidator(".com@gmail").is_email())

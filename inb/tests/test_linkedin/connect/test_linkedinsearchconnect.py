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
import json
import unittest

from unittest.mock import Mock
from unittest.mock import patch

from lib import ping
from errors import ConnectionLimitExceededException

from linkedin import Driver
from linkedin.DOM import JS
from linkedin.login import LinkedIn
from linkedin.connect import LinkedInSearchConnect


@unittest.skipUnless(ping("linkedin.com"), "linkedin.com server not responding")
class TestLinkedInSearchConnectClass(unittest.TestCase):
    def setUp(self: TestLinkedInSearchConnectClass) -> None:
        creds_abspath_ = os.path.dirname(
            os.path.abspath(__file__)) + "/../../creds/creds.json"
        with open(creds_abspath_, "r") as f:
            data = json.load(f)
        chrome_driver_options = []
        chrome_driver_options.append(Driver.HEADLESS)
        chrome_driver_options.append(
            Driver.DEFAULT_HEADLESS_WINDOW_SIZE)
        self.linkedin = LinkedIn(user_email=data["user_email"],
                                 user_password=data["user_password"],
                                 driver_path=data["driver_path"],
                                 opt_chromedriver_options=chrome_driver_options)

    def test_constructor_method_with_invalid_driver_instance_type(self: TestLinkedInSearchConnectClass) -> None:
        invalid_objs = [1, "ayush", [1, 2, 3, 4], {1: "ayush", 2: "mohika"}]
        for obj in invalid_objs:
            with self.assertRaises(TypeError):
                linkedinsearchconnect = LinkedInSearchConnect(obj)

    def test_contructor_method_with_invalid_limit_number(self: TestLinkedInSearchConnectClass) -> None:
        with self.assertRaises(ConnectionLimitExceededException):
            linkedinsearchconnect = LinkedInSearchConnect(
                self.linkedin.driver, limit=100)

    @patch("linkedin.DOM.JS.scroll_bottom")
    @patch("linkedin.DOM.JS.get_page_y_offset")
    def test_private_method_scroll(self: TestLinkedInSearchConnectClass,
                                   mock_js_get_page_y_offset: Mock,
                                   mock_js_scroll_bottom: Mock) -> None:
        linkedinsearchconnect = LinkedInSearchConnect(self.linkedin.driver)
        linkedinsearchconnect._scroll()
        mock_js_get_page_y_offset.assert_called()
        mock_js_scroll_bottom.assert_called()

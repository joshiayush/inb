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

from argparse import Namespace
from unittest.mock import Mock
from unittest.mock import patch

from lib.commandvalueparser import CommandValueParser


class TestCommandValueParserClass(unittest.TestCase):

    @patch("lib.commandvalueparser.CommandValueParser._send")
    def test_commandvalueparser_send_method(self: TestCommandValueParserClass, mock_private_send: Mock) -> None:
        email = "ayush854032@gmail.com"
        password = "xxx-xxx-xxx"
        limit = 20,
        cookies = True
        incognito = True
        headless = True
        start_maximezed = True
        which = "send"

        send_namespace = Namespace(email=email,
                                   password=password,
                                   limit=limit,
                                   cookies=cookies,
                                   incognito=incognito,
                                   headless=headless,
                                   start_maximized=start_maximezed,
                                   which=which)

        commandvalueparser = CommandValueParser(send_namespace)
        mock_private_send.assert_called_with(send_namespace)

        email = None
        password = None
        limit = 80,
        cookies = False
        incognito = False
        headless = False
        start_maximezed = False
        which = "send"

        send_namespace = Namespace(email=email,
                                   password=password,
                                   limit=limit,
                                   cookies=cookies,
                                   incognito=incognito,
                                   headless=headless,
                                   start_maximezed=start_maximezed,
                                   which=which)

        commandvalueparser = CommandValueParser(send_namespace)
        mock_private_send.assert_called_with(send_namespace)

    @patch("lib.commandvalueparser.CommandValueParser._connect")
    def test_commandvalueparser_connect_method(self: TestCommandValueParserClass, mock_private_connect: Mock) -> None:
        profileid = "aman-bisht-smart-boy"
        cookies = True
        incognito = True
        headless = True
        start_maximezed = True
        which = "connect"

        connect_namespace = Namespace(profileid=profileid,
                                      cookies=cookies,
                                      incognito=incognito,
                                      headless=headless,
                                      start_maximezed=start_maximezed,
                                      which=which)

        commandvalueparser = CommandValueParser(connect_namespace)
        mock_private_connect.assert_called_with(connect_namespace)

        profileid = None
        cookies = False
        incognito = False
        headless = False
        start_maximezed = False
        which = "connect"

        connect_namespace = Namespace(profileid=profileid,
                                      cookies=cookies,
                                      incognito=incognito,
                                      headless=headless,
                                      start_maximezed=start_maximezed,
                                      which=which)

        commandvalueparser = CommandValueParser(connect_namespace)
        mock_private_connect.assert_called_with(connect_namespace)

    @patch("lib.commandvalueparser.CommandValueParser._search")
    def test_commandvaluerparser_search_method(self: TestCommandValueParserClass, mock_private_search: Mock) -> None:
        email = "mohika@gmail.com"
        password = "xxx-xxx-xxx"
        keyword = "Doctor"
        location = "India"
        title = "NaN"
        first_name = "Mohika"
        last_name = "Negi"
        school = "B.R.M.S"
        industry = "Health Care"
        current_company = "NaN"
        profile_language = "English"
        limit = 1,
        cookies = True
        incognito = True
        headless = True
        start_maximized = True
        which = "search"

        search_namespace = Namespace(email=email,
                                     password=password,
                                     keyword=keyword,
                                     location=location,
                                     title=title,
                                     first_name=first_name,
                                     last_name=last_name,
                                     school=school,
                                     industry=industry,
                                     current_company=current_company,
                                     profile_langauge=profile_language,
                                     limit=limit,
                                     cookies=cookies,
                                     incognito=incognito,
                                     headless=headless,
                                     start_maximized=start_maximized,
                                     which=which)

        commandvalueparser = CommandValueParser(search_namespace)
        mock_private_search.assert_called_with(search_namespace)

        email = None
        password = None
        keyword = None
        location = None
        title = None
        first_name = None
        last_name = None
        school = None
        industry = None
        current_company = None
        profile_language = None
        limit = 80,
        cookies = True
        incognito = True
        headless = True
        start_maximized = True
        which = "search"

        search_namespace = Namespace(email=email,
                                     password=password,
                                     keyword=keyword,
                                     location=location,
                                     title=title,
                                     first_name=first_name,
                                     last_name=last_name,
                                     school=school,
                                     industry=industry,
                                     current_company=current_company,
                                     profile_langauge=profile_language,
                                     limit=limit,
                                     cookies=cookies,
                                     incognito=incognito,
                                     headless=headless,
                                     start_maximized=start_maximized,
                                     which=which)

        commandvalueparser = CommandValueParser(search_namespace)
        mock_private_search.assert_called_with(search_namespace)

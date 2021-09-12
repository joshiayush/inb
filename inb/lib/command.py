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

import logging
import argparse
import functools

from typing import Any
from typing import List
from typing import Dict

from selenium.common.exceptions import TimeoutException

from lib import ping
from lib import disable_log
from errors import InternetNotConnectedException

from linkedin import Driver
from linkedin.login import LinkedIn
from linkedin.connect import LinkedInConnect
from linkedin.connect import LinkedInConnectViaId
from linkedin.connect import LinkedInSearchConnect

from . import DRIVER_PATH
from .commandvalueparser import CommandValueParser


class Command(CommandValueParser):

    def __init__(self: Command, namespace: argparse.Namespace) -> None:
        super().__init__(namespace=namespace)

        disable_log("urllib3", logging.CRITICAL)
        logging.basicConfig(
            format="%(levelname)s:%(message)s", level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def _check_net_stat(function_: function) -> function:
        @functools.wraps(function_)
        def wrapper(self: Command, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
            nonlocal function_
            self.logger.info("Checking network status")
            if not ping("linkedin.com"):
                raise InternetNotConnectedException("Weak network found")
            self.logger.info("Internet is connected")
            function_(self, *args, **kwargs)
        return wrapper

    def _login(function_: function) -> function:
        @functools.wraps(function_)
        def wrapper(self: Command, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
            nonlocal function_
            chrome_driver_options: List[str] = []
            chrome_driver_options.append(Driver.INCOGNITO)
            chrome_driver_options.append(Driver.IGNORE_CERTIFICATE_ERRORS)
            if self.headless == True:
                chrome_driver_options.append(Driver.HEADLESS)

            self.linkedin = LinkedIn(user_email=self.email,
                                     user_password=self.password,
                                     driver_path=DRIVER_PATH,
                                     opt_chromedriver_options=chrome_driver_options)

            self.logger.info("Connecting")
            self.logger.info("Sending GET request to login page")
            self.logger.info("Logging in LinkedIn account (user-id=%(user_id)s)" %
                             {"user_id": self.email})
            try:
                self.linkedin.login()
            except TimeoutException as error:
                self.logger.critical(error)
                return
            else:
                self.logger.info("Successfully connected")
            function_(self, *args, **kwargs)
        return wrapper

    @_check_net_stat
    @_login
    def send(self: Command) -> None:
        self.logger.info("Instantiating connection object")
        linkedin_connection = LinkedInConnect(driver=self.linkedin.driver,
                                              limit=self.limit)
        self.logger.info("Sending GET request to mynetwork page")
        try:
            linkedin_connection.run()
        except TimeoutException as error:
            self.logger.critical(error)
            return

    @_check_net_stat
    @_login
    def connect(self: Command) -> None:
        self.logger.info("Instantiating connection object")
        linkedin_connect_id = LinkedInConnectViaId(driver=self.linkedin.driver,
                                                   person_id=self.personid)
        self.logger.info("Sending GET request to person's profile page")
        try:
            linkedin_connect_id.run()
        except TimeoutException as exc:
            self.logger.critical(exc)
            return

    @_check_net_stat
    @_login
    def search(self: Command) -> None:
        self.logger.info("Instantiating connection object")
        linkedin_search_connect = LinkedInSearchConnect(
            driver=self.linkedin.driver,
            keyword=self.keyword,
            location=self.location,
            title=self.title,
            first_name=self.first_name,
            last_name=self.last_name,
            school=self.school,
            industry=self.industry,
            current_company=self.current_company,
            profile_language=self.profile_language,
            limit=self.limit)
        self.logger.info("Sending GET request to search results page")
        linkedin_search_connect.run()

    def show(self: Command) -> None:
        self.logger.info("facility not present")

    def config(self: Command) -> None:
        self.logger.info("facility not present")

    def delete(self: Command) -> None:
        self.logger.info("facility not present")

    def developer(self: Command) -> None:
        self.logger.info("facility not present")

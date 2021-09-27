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

import time
import logging
import functools

from typing import Any, Union
from typing import List
from typing import Dict

from lib import _type
from lib import is_int
from lib import is_str
from lib import __project_name__

from ..person.person import Person
from ..DOM.cleaners import Cleaner
from ..invitation.status import Invitation

from errors import ConnectionLimitExceededException

from selenium import webdriver

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.webdriver.common.action_chains import ActionChains


class LinkedInConnect(object):
    __INVITATION_SENT: int = 0
    MY_NETWORK_PAGE: str = "https://www.linkedin.com/mynetwork/"

    def __init__(
        self: LinkedInConnect,
        driver: webdriver.Chrome,
        limit: int = 40,
        debug: bool = False
    ) -> None:
        """LinkedInConnectionsAuto class constructor to initialise LinkedInConnectionsAuto object.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - driver: {webdriver.Chrome} chromedriver instance
            - limit: {int} daily invitation limit

        :Returns:
            - {LinkedInConnectionsAuto} LinkedInConnectionsAuto object

        :Raises:
            - ConnectionLimitExceededException if user gives a connection limit that exceeds 80
        """
        if debug == True:
            self._set_logger(logging.DEBUG)
        else:
            self._set_logger()

        if not isinstance(driver, webdriver.Chrome):
            raise Exception(
                "Object '%(driver)s' is not a 'webdriver.Chrome' object!" % {
                    "driver": _type(driver)})
        self._driver = driver
        self.logger.debug("Private driver instance: %(driver)s" %
                          {"driver": self._driver})

        if limit > 80:
            raise ConnectionLimitExceededException(
                "Daily invitation limit can't be greater than 80, we recommend 40!")
        self._limit = limit
        self.logger.debug("Private limit variable: %(limit)s" %
                          {"limit": self._limit})

    def _set_logger(self: LinkedInConnect, level: Union[int, str] = logging.INFO) -> None:
        logging.basicConfig(format="%(levelname)s:%(message)s")
        self.logger = logging.getLogger(__project_name__)
        if is_int(level) or is_str(level):
            self.logger.setLevel(level)
        else:
            self.logger.setLevel(logging.INFO)

    def _get_mynetwork(function_: function) -> None:
        """Method get_my_network() sends a GET request to the network page of LinkedIn.

        :Args:
            - self: {LinkedInConnectionsAuto} object
            - _url: {str} url to send GET request to

        :Returns:
            - {None}

        :Raises:
            - EmptyResponseException if there is a TimeoutException
        """
        @functools.wraps(function_)
        def wrapper(self: LinkedInConnect, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
            nonlocal function_
            try:
                self.logger.debug("Calling chromedriver.get() method with url: %(url)s" % {
                                  "url": LinkedInConnect.MY_NETWORK_PAGE})
                self._driver.get(LinkedInConnect.MY_NETWORK_PAGE)
            except TimeoutException:
                raise TimeoutException(
                    "ERR: Cannot get mynetwork page due to weak network!")
            else:
                self.logger.debug("Calling decorated method with args %(args)s and kwargs %(kwargs)s" % {
                                  "args": [*args], "kwargs": {**kwargs}})
                function_(self, *args, **kwargs)
        return wrapper

    def _send_invitation(self: LinkedInConnect) -> None:
        """Method send_invitation() starts sending invitation to people on linkedin.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        start = time.time()
        self.logger.debug(
            "Method send invitation starting at %(time)s" % {"time": start})

        p = Person(self._driver)
        person = p.get_suggestion_box_element()
        self.logger.debug("Initial value of Person object: %(obj)s" % {
                          "obj": {"name": person.name, "occupation": person.occupation,
                                  "connect_button": person.connect_button}})

        while person:
            self.logger.debug("LinkedInConnect.__INVITATION_SENT: %(num)s" % {
                              "num": LinkedInConnect.__INVITATION_SENT})
            if LinkedInConnect.__INVITATION_SENT == self._limit:
                break

            try:
                ActionChains(self._driver).move_to_element(
                    person.connect_button).click().perform()
                Invitation(name=person.name,
                           occupation=person.occupation,
                           status="sent",
                           elapsed_time=time.time() - start).status()
                LinkedInConnect.__INVITATION_SENT += 1
            except (ElementNotInteractableException,
                    ElementClickInterceptedException) as error:
                if isinstance(error, ElementClickInterceptedException):
                    break
                Invitation(name=person.name,
                           occupation=person.occupation,
                           status="failed",
                           elapsed_time=time.time() - start).status()

            person = p.get_suggestion_box_element()
            self.logger.debug("Next value of Person object: %(obj)s" % {
                "obj": {"name": person.name, "occupation": person.occupation,
                        "connect_button": person.connect_button}})

    def _execute_cleaners(self: LinkedInConnect) -> None:
        """Method execute_cleaners() scours the unwanted element from the page during the
        connect process.

        :Args:
            - self: {LinkedInConnectionsAuto}

        :Returns:
            - {None}
        """
        self.logger.debug("Calling Cleaner's clear_message_overlay method")
        Cleaner(self._driver).clear_message_overlay()

    @_get_mynetwork
    def run(self: LinkedInConnect) -> None:
        """Method run() calls the send_invitation method, but first it assures that the object
        self has driver property in it.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        self._execute_cleaners()
        self._send_invitation()

    def __del__(self: LinkedInConnect) -> None:
        """LinkedInConnectionsAuto destructor to de-initialise LinkedInConnectionsAuto object.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        LinkedInConnect.__INVITATION_SENT = 0
        self.logger.debug("LinkedInConnect.__INVITATION_SENT on __del__: %(num)s" % {
                          "num": LinkedInConnect.__INVITATION_SENT})
        self._driver.quit()
        self.logger.debug("Successfully called quit method on driver instance")

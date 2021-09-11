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

import re
import functools

from typing import Any
from typing import List
from typing import Dict

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

from lib import _type

from ..DOM import Cleaner
from ..person.person import Person
from ..invitation.status import Invitation


class LinkedInConnectViaId(object):
    WAIT: int = 60
    BASE_URL: str = "https://www.linkedin.com/in/"

    def __init__(self: LinkedInConnectViaId, driver: webdriver.Chrome, person_id: str) -> None:
        if not isinstance(driver, webdriver.Chrome):
            raise Exception(
                "Object '%(driver)s' is not a 'webdriver.Chrome' object!" % {
                    "driver": _type(driver)})
        self._driver = driver

        _re = re.compile(r"([a-z]+-?)+([a-zA-Z0-9]+)?", re.IGNORECASE)
        if not _re.search(person_id).group(0):
            raise Exception(
                "LinkedInConnectViaId: Parameter provided is not a valid person id!")
        self.id_url = self.BASE_URL + person_id + "/"

    def _get_person_profile(function_: function) -> function:
        @functools.wraps(function_)
        def wrapper(self: LinkedInConnectViaId, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
            nonlocal function_
            try:
                self._driver.get(self.id_url)
            except TimeoutException:
                raise TimeoutException(
                    "ERR: Cannot get person profile page due to weak network!")
            else:
                function_(self, *args, **kwargs)
        return wrapper

    def __execute_cleaners(self: LinkedInConnectViaId) -> None:
        """Method execute_cleaners() scours the unwanted element from the page during the
        connect process.

        :Args:
            - self: {LinkedInConnectionsAuto}

        :Returns:
            - {None}
        """
        Cleaner(self._driver).clear_message_overlay()

    def __send_invitation(self: LinkedInConnectViaId) -> None:
        p = Person(self._driver)
        person = p.get_profile_element()

        try:
            ActionChains(self._driver).move_to_element(
                person.connect_button).click().perform()
            Invitation(name=person.name,
                       occupation=person.occupation,
                       status="sent").status()
        except (ElementNotInteractableException,
                ElementClickInterceptedException) as exc:
            if isinstance(exc, ElementClickInterceptedException):
                return
            Invitation(name=person.name,
                       occupation=person.occupation,
                       status="failed").status()

    @_get_person_profile
    def run(self: LinkedInConnectViaId) -> None:
        self.__execute_cleaners()
        self.__send_invitation()

    def __del__(self: LinkedInConnectViaId) -> None:
        self._driver.quit()

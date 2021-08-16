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

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import sys
import time
import json

from typing import Union
from typing import TextIO

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from . import Path_To_Element_By

from .DOM.javascript import JS


class Person_Info(object):
    """Class Person_Info provides an object with person's necessary details fetched
    from linkedin's page.
    """
    BASE_LINKEDIN_URL: str = "https://www.linkedin.com"

    def __init__(
            self: Person_Info,
            name: Union[str, None] = None,
            occupation: Union[str, None] = None,
            profile_url: Union[str, None] = None,
            photo_url: Union[str, None] = None,
            connect_button: Union[webdriver.Chrome, None] = None
    ) -> None:
        """Constructor method initializes the Person_Info object with basic details
        about the person.

        :Args:
            - self: {Person_Info} self.
            - name: {str} person's name.
            - occupation: {str} person's occupation.
            - profile_url: {str} person's linkedin profile url.
            - photo_url: {str} person's linkedin profile photo url.
            - connect_button: {webdriver.Chrome} person's connect button instance.
        """
        self._name = name
        self._occupation = occupation
        self._profile_url = profile_url
        self._photo_url = photo_url
        self._connect_button = connect_button
        self._person_id = self.person_id()

    def person_id(self: Person_Info) -> str:
        """Method person_id() returns the person id filtering the person's profile url.

        :Args:
            - self: {Person_Info} self.

        :Returns:
            - {str} person id.
        """
        _url_base: str = self.BASE_LINKEDIN_URL + "/in/"
        _indx: int = self._profile_url.find(_url_base) + len(_url_base)

        _profile_url: str = self._profile_url

        while not _profile_url[_indx] == '/':
            _indx += 1
        _indx -= 1

        _id: str = ''
        while not _profile_url[_indx] == '-' and not _profile_url[_indx] == '/':
            _id += _profile_url[_indx]
            _indx -= 1

        return _id[::-1]

    def freeze(
        self: Person_Info,
        file: Union[str, TextIO] = sys.stdout,
        mode: str = "w",
        _format: str = None
    ) -> None:
        """Method freeze() dumps the current object state in the given file in the given format.

        :Args:
            - self: {Person_Info} self.
            - file: {Union[str, TextIO]} file to dump the current object state in.
            - mode: {str} in what mode to open the file in.
            - _format: {str} in what format to write the data in.

        :Raises:
            - {Exception} if the format and the file is not identified.
        """
        _message: str = ''

        if _format == "json":
            _message = json.dump({
                "name": self._name,
                "person_id": self._person_id,
                "occupation": self._occupation,
                "profile_url": self._profile_url,
                "photo_url": self._photo_url
            })
        elif _format == "raw":
            _message = ("name: %(name)s\n" +
                        "person_id: %(person_id)s\n" +
                        "occupation: %(occupation)s\n" +
                        "profile_url: %(profile_url)s\n" +
                        "photo_url: %(photo_url)s") % {
                "name": self._name,
                "person_id": self._person_id,
                "occupation": self._occupation,
                "profile_url": self._profile_url,
                "photo_url": self._photo_url}
        else:
            raise Exception("Format '%(frmt)s' is not supported!" %
                            {"frmt": _format})

        if isinstance(file, str):
            with open(file=file, mode=mode) as file:
                if file.endswith(".json"):
                    json.dump(_message, file, indent=2)
                else:
                    file.write(_message)
            return
        elif file == sys.stdout:
            file.write(_message)
        else:
            raise Exception("File '%(file)s' is not supported!" %
                            {"file": file})


class Person(object):
    """Class Person to target the person element on the page."""

    def __init__(self: Person, driver: webdriver.Chrome) -> None:
        """Constructor method to initialize the driver instance and element count.

        :Args:
            - self: {Person} self.
            - driver: {webdriver.Chrome} chromedriver instance.

        :Raises:
            - {Exception} if the driver object in not identified.
        """
        if not isinstance(driver, webdriver.Chrome):
            raise Exception("'%(driver_type)s' object is not a 'webdriver' object" % {
                            "driver_type": type(driver)})

        self._driver = driver
        self.__suggestion_box_element_count = 0

    def __load_page(self: Person) -> None:
        """Private method __load_page() loads the page by scrolling it down.

        :Args:
            - self: {Person} self

        :Returns:
            - {None}
        """
        _js = JS(self._driver)

        _old_page_offset = _js.get_page_y_offset()
        _new_page_offset = _js.get_page_y_offset()

        while _old_page_offset == _new_page_offset:
            _js.scroll_bottom()
            time.sleep(1)
            _new_page_offset = _js.get_page_y_offset()

    def get_suggestion_box_element(self: Person):
        """Method get_suggestion_box_element() an object containing the person details
        including the connect button to connect with the person.

        :Args:
            - self: {Person} self.

        :Returns:
            - {Person_Info} person object.
        """
        def get_suggestion_box_person_li() -> webdriver.Chrome:
            """Nested function get_suggestion_box_person() finds the actual element that
            wraps the person on the page.

            :Args:
                - {None}

            :Return:
                - {webdriver.Chrome} element that wraps the person.
            """
            # Using parent function 'self' variable
            nonlocal self

            # Traget the element using its root xpath
            _xpath: str = Path_To_Element_By.SUGGESTION_BOX_ELEMENT_XPATH
            # Update the xpath every time the function is called to target the next element
            _xpath = _xpath[:-3] + '[' + \
                str(self.__suggestion_box_element_count + 1) + ']'

            if self.__suggestion_box_element_count == 0:
                self.__load_page()

            self.__suggestion_box_element_count += 1

            while True:
                try:
                    return WebDriverWait(self._driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, _xpath))
                    )
                except (TimeoutException, NoSuchElementException) as error:
                    if isinstance(error, TimeoutException):
                        self.__load_page()
                    continue

        def transform_to_object(li: webdriver.Chrome) -> Person_Info:
            """Nested function transform_to_object() gets the person's details from the element
            that wraps the person and transform into an Person_Info object.

            :Args:
                - li: {webdriver.Chrome} element to get the person details from

            :Returns:
                - {Person_Info}
            """
            # Target the info container that is inside of the element we are given
            _info_container: webdriver.Chrome = li.find_element_by_css_selector(
                "div[class='discover-entity-type-card__info-container']")
            # Target the anchor tag from the info container to later get the image url
            # and the profile url of the person
            _anchor_tag: webdriver.Chrome = _info_container.find_element_by_tag_name(
                "a")
            # Target the image element to get the image url later
            _img_tag: webdriver.Chrome = _anchor_tag.find_element_by_tag_name(
                "img")
            # Target the bottom container inside of the info container to target the connect
            # button
            _bottom_container: webdriver.Chrome = li.find_element_by_css_selector(
                "div[class^='discover-entity-type-card__bottom-container']")
            # Target the footer element inside of the bottom container to get the connect button
            _footer: webdriver.Chrome = _bottom_container.find_element_by_tag_name(
                "footer")

            # Get the person's name from the element inside of the anchor tag
            _person_name: str = _anchor_tag.find_element_by_css_selector(
                "span[class^='discover-person-card__name']").text
            # Get the person's occupation from the element inside of the anchor tag
            _person_occupation: str = _anchor_tag.find_element_by_css_selector(
                "span[class^='discover-person-card__occupation']").text
            # Get the person's photo url from the image tag
            _person_photo_url: str = _img_tag.get_attribute("src")
            # Get the person's profile url from the anchor tag
            _person_profile_url: str = "%(profile_path)s" % {
                "profile_path": _anchor_tag.get_attribute("href")}
            # Get the connect button from the footer element
            _person_connect_button: str = _footer.find_element_by_css_selector(
                f"button[aria-label^='Invite']")

            return Person_Info(
                name=_person_name,
                occupation=_person_occupation,
                profile_url=_person_profile_url,
                photo_url=_person_photo_url,
                connect_button=_person_connect_button
            )

        return transform_to_object(get_suggestion_box_person_li())

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

import time

from typing import Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from . import Path_To_Element_By

from .DOM.javascript import JS


class Person_Info(object):
    BASE_LINKEDIN_URL: str = "https://www.linkedin.com"

    def __init__(
            self: Person_Info,
            name: Union[str, None] = None,
            occupation: Union[str, None] = None,
            profile_url: Union[str, None] = None,
            photo_url: Union[str, None] = None,
            connect_button: Union[webdriver.Chrome, None] = None
    ) -> None:
        self._name = name
        self._occupation = occupation
        self._profile_url = profile_url
        self._photo_url = photo_url
        self._connect_button = connect_button
        self._person_id = self.person_id()

    def person_id(self: Person_Info) -> str:
        _url_base: str = self.BASE_LINKEDIN_URL + "/in/"
        _indx: int = self._profile_url.find(_url_base) + len(_url_base)

        _profile_url: str = self._profile_url

        while not _profile_url[_indx] == '/':
            _indx += 1

        _indx += 1
        _id: str = ''

        while not _profile_url[_indx] == '/' or not _profile_url[_indx] == '-':
            _id += _profile_url[_indx]
            _indx -= 1

        return _id[::-1]

    def freeze(
        self: Person_Info,
        file: str = None,
        format: str = None
    ) -> None:
        pass


class Person(object):
    def __init__(self: Person, driver: webdriver.Chrome) -> None:
        if not isinstance(driver, webdriver.Chrome):
            raise Exception("'%(driver_type)s' object is not a 'webdriver' object" % {
                            "driver_type": type(driver)})

        self._driver = driver
        self.__suggestion_box_element_count = 0

    def __load_page(self: Person) -> None:
        """Method __load_page() loads the page by scrolling it down.

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
        def get_suggestion_box_person_li() -> webdriver.Chrome:
            nonlocal self

            _xpath: str = Path_To_Element_By.SUGGESTION_BOX_ELEMENT_XPATH
            _xpath = _xpath[:-3] + '[' + \
                str(self.__suggestion_box_element_count + 1) + ']'

            self.__suggestion_box_element_count += 1
            self.__load_page()

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
            _info_container: webdriver.Chrome = li.find_element_by_css_selector(
                "div[class='discover-entity-type-card__info-container']")
            _anchor_tag: webdriver.Chrome = _info_container.find_element_by_tag_name(
                "a")
            _img_tag: webdriver.Chrome = _anchor_tag.find_element_by_tag_name(
                "img")
            _bottom_container: webdriver.Chrome = li.find_element_by_css_selector(
                "div[class^='discover-entity-type-card__bottom-container']")
            _footer: webdriver.Chrome = _bottom_container.find_element_by_tag_name(
                "footer")

            _person_name: str = _anchor_tag.find_element_by_css_selector(
                "span[class^='discover-person-card__name']").text
            _person_occupation: str = _anchor_tag.find_element_by_css_selector(
                "span[class^='discover-person-card__occupation']").text
            _person_photo_url: str = _img_tag.get_attribute("src")
            _person_profile_url: str = "%(base_url)s%(profile_path)s" % {
                "base_url": Person_Info.BASE_LINKEDIN_URL,
                "profile_path": _anchor_tag.get_attribute("href")}
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

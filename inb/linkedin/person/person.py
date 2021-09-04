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
from typing import List

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from . import Person_Info

from . import Path_To_Element_By
from ..DOM.javascript import JS


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
            # first target the html elements that holds the actual details of a person
            # that we are interested in
            info_container = li.find_element_by_css_selector(
                "div[class='discover-entity-type-card__info-container']")
            anchor_tag = info_container.find_element_by_tag_name("a")
            img_tag = anchor_tag.find_element_by_tag_name("img")
            bottom_container = li.find_element_by_css_selector(
                "div[class^='discover-entity-type-card__bottom-container']")
            footer = bottom_container.find_element_by_tag_name("footer")

            # target the actual values from the html elements that we get from the above
            # operations and store them to later create a Person_Info object with these
            # details
            person_name = anchor_tag.find_element_by_css_selector(
                "span[class^='discover-person-card__name']").text
            person_occupation = anchor_tag.find_element_by_css_selector(
                "span[class^='discover-person-card__occupation']").text
            person_photo_url = img_tag.get_attribute("src")
            person_profile_url = "%(profile_path)s" % {
                "profile_path": anchor_tag.get_attribute("href")}
            person_connect_button = footer.find_element_by_css_selector(
                f"button[aria-label^='Invite']")

            return Person_Info(
                name=person_name,
                occupation=person_occupation,
                profile_url=person_profile_url,
                photo_url=person_photo_url,
                connect_button=person_connect_button)

        return transform_to_object(get_suggestion_box_person_li())

    def get_search_results_elements(self: Person) -> List[Person_Info]:
        def get_search_results_person_lis() -> List[webdriver.Chrome]:
            # Using parent function 'self' variable
            nonlocal self

            _target: int = 1

            # Traget the element using its relative xpath
            _xpath: str = Path_To_Element_By.SEARCH_RESULTS_PEOPLE_XPATH

            _search_results_person_lis: List[webdriver.Chrome] = []

            while True:
                # Update the xpath in each iteration
                _xpath = _xpath[:-3] + '[' + str(_target) + ']'
                try:
                    _search_results_person_lis.append(WebDriverWait(self._driver, 0.5).until(
                        EC.presence_of_element_located((By.XPATH, _xpath))
                    ))
                except (TimeoutException, NoSuchElementException) as exc:
                    if isinstance(exc, NoSuchElementException):
                        break
                    continue
                _target += 1
                if _target > 10:
                    break

            return _search_results_person_lis

        def transform_to_object(lis: List[webdriver.Chrome]) -> List[Person_Info]:
            person_infos: List[Person_Info] = []

            for li in lis:
                entity_result_item_container = li.find_element_by_tag_name(
                    "div").find_element_by_css_selector("div[class='entity-result__item']")
                entity_result_image_container = entity_result_item_container.find_element_by_css_selector(
                    "div[class='entity-result__image']")

                entity_result_anchor_tag = entity_result_image_container.find_element_by_tag_name("a")
                person_profile_url = entity_result_anchor_tag.get_attribute("href")
                entity_result_img_tag = entity_result_image_container.find_element_by_xpath("//div/a/div[1]/div[1]/img[1]")
                person_photo_url = entity_result_img_tag.get_attribute("src")

                entity_result_content_container = entity_result_item_container.find_element_by_css_selector(
                    "div[class^='entity-result__content']")
                try:
                    person_occupation = entity_result_content_container.find_element_by_css_selector(
                        "div[class^='entity-result__primary-subtitle']").text
                except NoSuchElementException:
                    person_occupation = ''
                try:
                    person_location = entity_result_content_container.find_element_by_css_selector(
                        "div[class^='entity-result__secondary-subtitle']").text
                except NoSuchElementException:
                    person_location = ''
                try:
                    person_summary = entity_result_content_container.find_element_by_css_selector(
                        "p[class^='entity-result__summary']").text
                except NoSuchElementException:
                    person_summary = ''

                entity_result_content_anchor_tag = entity_result_content_container.find_element_by_tag_name("a")
                person_name = entity_result_content_anchor_tag.text

                person_connect_button = entity_result_item_container.find_element_by_css_selector(
                    "div[class^='entity-result__actions']").find_element_by_tag_name("button")

                person_infos.append(Person_Info(
                    name=person_name,
                    occupation=person_occupation,
                    photo_url=person_photo_url,
                    profile_url=person_profile_url,
                    location=person_location,
                    summary=person_summary,
                    connect_button=person_connect_button
                ))

            return person_infos

        return transform_to_object(get_search_results_person_lis())

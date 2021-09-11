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

from typing import Any
from typing import List
from typing import Dict
from typing import Optional

from selenium import webdriver

from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from errors import ConnectionLimitExceededException

from lib.algo import levenshtein
from lib.utils import _type

from ..DOM import Cleaner
from ..person.person import Person
from ..invitation.status import Invitation


class LinkedInSearchConnect(object):
    """Class LinkedInSearchConnect() will search people based on the given Keyword,
    Location, Current Company, School, Industry, Profile Language, First Name,
    Last Name, Title."""
    WAIT: int = 60
    __INVITATION_SENT: int = 0

    def __init__(
        self: LinkedInSearchConnect,
        driver: webdriver.Chrome,
        keyword: str,
        location: str,
        title: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
        school: Optional[str],
        industry: Optional[str],
        current_company: Optional[str],
        profile_language: Optional[str],
        limit: int = 40
    ) -> None:
        """Constructor method to initialize LinkedInSearchConnect instance.

        :Args:
            - self: {LinkedInSearchConnect} self.
            - driver: {webdriver.Chrome} chromedriver instance.
            - keyword: {str} keyword to search for.
            - location: {str} location to search the keyword in.
            - title: {str} person occupation (Optional).
            - first_name: {str} person first name (Optional).
            - last_name: {str} person last name (Optional).
            - school: {str} person school (Optional).
            - industry: {str} person's industry (Optional).
            - current_company: {str} person's current company (Optional).
            - profile_language: {str} person's profile language (Optional).

        :Raises:
            - {Exception}
            - {ConnectionLimitExceededException}
        """
        if not isinstance(driver, webdriver.Chrome):
            raise Exception(
                "Object '%(driver)s' is not a 'webdriver.Chrome' object!" % {
                    "driver": _type(driver)})
        self._driver = driver

        if limit > 80:
            raise ConnectionLimitExceededException(
                "Daily invitation limit can't be greater than 80, we recommend 40!")
        self._limit = limit

        self._keyword = keyword
        self._location = location
        self._title = title
        self._first_name = first_name
        self._last_name = last_name
        self._school = school
        self._industry = industry
        self._current_company = current_company
        self._profile_language = profile_language

    def _get_search_results_page(function_: function) -> function:
        def run(self: LinkedInSearchConnect, *args: List[Any], **kwargs: Dict[Any, Any]) -> None:
            nonlocal function_
            search_box: webdriver.Chrome = WebDriverWait(self._driver, 60).until(
                EC.presence_of_element_located(
                    (By.XPATH, """//*[@id="global-nav-typeahead"]/input"""))
            )
    
            search_box.clear()
            search_box.send_keys(self._keyword)
            search_box.send_keys(Keys.RETURN)
            function_(self, *args, **kwargs)
        return run

    def __execute_cleaners(self: LinkedInSearchConnect) -> None:
        """Method execute_cleaners() scours the unwanted element from the page during the
        connect process.

        :Args:
            - self: {LinkedInConnectionsAuto}

        :Returns:
            - {None}
        """
        Cleaner(self._driver).clear_message_overlay()

    def __apply_filters(self: LinkedInSearchConnect):
        def get_element_by_xpath(xpath: str, wait: int = None) -> webdriver.Chrome:
            if wait == None:
                wait = LinkedInSearchConnect.WAIT
            return WebDriverWait(self._driver, wait).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

        def get_elements_by_xpath(xpath: str, wait: int = None) -> webdriver.Chrome:
            if wait == None:
                wait = LinkedInSearchConnect.WAIT
            return WebDriverWait(self._driver, wait).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )

        people_button = get_element_by_xpath(
            "//div[@id='search-reusables__filters-bar']//button[@aria-label='People']")
        people_button.click()
        del people_button

        if self._location or self._industry or self._profile_language or self._first_name or \
                self._last_name or self._title or self._current_company or self._school:
            filters_button = get_element_by_xpath(
                "//div[@id='search-reusables__filters-bar']//button[@aria-label='All filters']")
            filters_button.click()
            del filters_button

        def check_for_filter(filter: str,
                             filter_dict: Dict[str, webdriver.Chrome],
                             threshold: float = 80.0) -> None:
            if isinstance(filter, str):
                if filter in filter_dict:
                    filter_dict[filter].click()
                    return
                for fltr in filter_dict.keys():
                    levenshtein_dis = levenshtein(filter, fltr)
                    total_str_len = (len(filter) + len(fltr))
                    levenshtein_dis_percent = (
                        (total_str_len - levenshtein_dis) / total_str_len) * 100
                    if levenshtein_dis_percent >= threshold:
                        filter_dict[fltr].click()
                return

            if isinstance(filter, list):
                filters_present: List[str] = filter_dict.keys()
                for fltr in filter:
                    if fltr in filters_present:
                        filter_dict[fltr].click()
                        continue
                    for _fltr in filters_present:
                        levenshtein_dis = levenshtein(fltr, _fltr)
                        total_str_len = (len(fltr) + len(_fltr))
                        levenshtein_dis_percent = (
                            (total_str_len - levenshtein_dis) / total_str_len) * 100
                        if levenshtein_dis_percent >= threshold:
                            filter_dict[_fltr].click()
                return

        if self._location:
            location_inps = get_elements_by_xpath(
                "//input[starts-with(@id, 'advanced-filter-geoUrn-')]")
            location_labels = get_elements_by_xpath(
                "//label[starts-with(@for, 'advanced-filter-geoUrn-')]")
            locations: List[str] = [label.find_element_by_tag_name("span").text
                                    for label in location_labels]
            del location_labels
            locations_dict: Dict[str, webdriver.Chrome]
            for location, location_inp in zip(locations, location_inps):
                locations_dict[location] = location_inp
            del locations
            del location_inps

            check_for_filter(self._location, locations_dict)
            del locations_dict

        if self._industry:
            industry_inps = get_elements_by_xpath(
                "//input[starts-with(@id, 'advanced-filter-industry-')]")
            industry_labels = get_elements_by_xpath(
                "//label[starts-with(@for, 'advanced-filter-industry-')]")
            industries: List[str] = [label.find_element_by_tag_name("span").text
                                     for label in industry_labels]
            del industry_labels
            industries_dict: Dict[str, webdriver.Chrome]
            for industry, industry_inp in zip(industries, industry_inps):
                industries_dict[industry] = industry_inp
            del industries
            del industry_inps

            check_for_filter(self._industry, industries_dict)
            del industries_dict

        if self._profile_language:
            profile_language_inps = get_elements_by_xpath(
                "//input[starts-with(@id, 'advanced-filter-profileLanguage-')]")
            profile_language_labels = get_elements_by_xpath(
                "//label[starts-with(@for, 'advanced-filter-profileLanguage-')]")
            profile_languages: List[str] = [label.find_element_by_tag_name("span").text
                                            for label in profile_language_labels]
            del profile_language_labels
            profile_languages_dict: Dict[str, webdriver.Chrome]
            for profile_language, profile_language_inp in zip(profile_languages, profile_language_inps):
                profile_languages_dict[profile_language] = profile_language_inp
            del profile_languages
            del profile_language_inps

            check_for_filter(self._profile_language, profile_languages_dict)
            del profile_languages_dict

        if self._first_name:
            first_name_box = get_elements_by_xpath(
                "//label[contains(text(), 'First name')]").find_element_by_tag_name("input")
            first_name_box.clear()
            first_name_box.send_keys(self._first_name)
            del first_name_box

        if self._last_name:
            last_name_box = get_element_by_xpath(
                "//label[contains(text(), 'Last name')]").find_element_by_tag_name("input")
            last_name_box.clear()
            last_name_box.send_keys(self._last_name)
            del last_name_box

        if self._title:
            title_box = get_element_by_xpath(
                "//label[contains(text(), 'Title')]").find_element_by_tag_name("input")
            title_box.clear()
            title_box.send_keys(self._title)
            del title_box

        if self._current_company:
            company_box = get_element_by_xpath(
                "//label[contains(text(), 'Company')]").find_element_by_tag_name("input")
            company_box.clear()
            company_box.send_keys(self._current_company)
            del company_box

        if self._school:
            school_box = get_element_by_xpath(
                "//label[contains(text(), 'School')]").find_element_by_tag_name("input")
            school_box.clear()
            school_box.send_keys(self._school)
            del school_box

        if self._location or self._industry or self._profile_language or self._first_name or \
                self._last_name or self._title or self._current_company or self._school:
            show_results_button = get_element_by_xpath(
                "//div[@id='artdeco-modal-outlet']//button[@aria-label='Apply current filters to show results']")
            show_results_button.click()
            del show_results_button

    def __send_invitation(self: LinkedInSearchConnect) -> None:
        start = time.time()

        p = Person(self._driver)
        persons = p.get_search_results_elements()

        while True:
            for person in persons:
                if LinkedInSearchConnect.__INVITATION_SENT == self._limit:
                    break
                if person._connect_button.text == "Pending" or \
                        person._connect_button.get_attribute("aria-label") == "Follow":
                    continue

                try:
                    ActionChains(self._driver).move_to_element(
                        person._connect_button).click().perform()
                    send_invite_modal = WebDriverWait(self._driver, LinkedInSearchConnect.WAIT).until(
                        EC.presence_of_element_located(
                            (By.XPATH,
                             "//div[@aria-labelledby='send-invite-modal']")
                        )
                    )
                    send_now = send_invite_modal.find_element_by_xpath(
                        "//button[@aria-label='Send now']")
                    ActionChains(self._driver).move_to_element(
                        send_now).click().perform()
                    Invitation(name=person._name,
                               occupation=person._occupation,
                               status="sent",
                               elapsed_time=time.time() - start).status()
                    LinkedInSearchConnect.__INVITATION_SENT += 1
                except (ElementNotInteractableException,
                        ElementClickInterceptedException) as exc:
                    if isinstance(exc, ElementClickInterceptedException):
                        break
                    Invitation(name=person._name,
                               occupation=person._occupation,
                               status="failed",
                               elapsed_time=time.time() - start).status()

            _next: webdriver.Chrome = self._driver.find_element_by_xpath(
                "//main[@id='main']//button[@aria-label='Next']")
            _next.click()
            persons = p.get_search_results_elements()

    @_get_search_results_page
    def run(self: LinkedInSearchConnect) -> None:
        """Method run() calls the send_invitation method, but first it assures that the object
        self has driver property in it.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        self.__apply_filters()
        self.__execute_cleaners()
        self.__send_invitation()

    def __del__(self: LinkedInSearchConnect) -> None:
        """LinkedInConnectionsAuto destructor to de-initialise LinkedInConnectionsAuto object.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        LinkedInSearchConnect.__INVITATION_SENT = 0
        self._driver.quit()

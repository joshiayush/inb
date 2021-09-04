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

from .DOM import Cleaner
from .person.person import Person
from .invitation.status import Invitation


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

    def __get_search_results_page(self: LinkedInSearchConnect) -> None:
        _search_box: webdriver.Chrome = WebDriverWait(self._driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, """//*[@id="global-nav-typeahead"]/input"""))
        )

        _search_box.clear()
        _search_box.send_keys(self._keyword)
        _search_box.send_keys(Keys.RETURN)

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

        _people_button: webdriver.Chrome = get_element_by_xpath(
            "//div[@id='search-reusables__filters-bar']//button[@aria-label='People']")
        _people_button.click()
        del _people_button

        if self._location or self._industry or self._profile_language or self._first_name or \
                self._last_name or self._title or self._current_company or self._school:
            _filters_button: webdriver.Chrome = get_element_by_xpath(
                "//div[@id='search-reusables__filters-bar']//button[@aria-label='All filters']")
            _filters_button.click()
            del _filters_button

        def check_for_filter(
                _filter: str,
                _filter_dict: Dict[str, webdriver.Chrome],
                _threshold: float = 80.0
        ) -> None:
            if isinstance(_filter, str):
                if _filter in _filter_dict:
                    _filter_dict[_filter].click()
                else:
                    for fltr in _filter_dict.keys():
                        _levenshtein_dis: int = levenshtein(
                            _filter, fltr)
                        _total_str_len: int = (len(_filter) + len(fltr))
                        _levenshtein_dis_percent: float = (
                            (_total_str_len - _levenshtein_dis) / _total_str_len) * 100
                        if _levenshtein_dis_percent >= _threshold:
                            _filter_dict[fltr].click()
            elif isinstance(_filter, list):
                _filters_present: List[str] = _filter_dict.keys()
                for fltr in _filter:
                    if fltr in _filters_present:
                        _filter_dict[fltr].click()
                    else:
                        for _fltr in _filters_present:
                            _levenshtein_dis: int = levenshtein(
                                fltr, _fltr)
                            _total_str_len: int = (len(fltr) + len(_fltr))
                            _levenshtein_dis_percent: float = (
                                (_total_str_len - _levenshtein_dis) / _total_str_len) * 100
                            if _levenshtein_dis_percent >= _threshold:
                                _filter_dict[_fltr].click()

        if self._location:
            _location_inps: webdriver.Chrome = get_elements_by_xpath(
                "//input[starts-with(@id, 'advanced-filter-geoUrn-')]")
            _location_labels: webdriver.Chrome = get_elements_by_xpath(
                "//label[starts-with(@for, 'advanced-filter-geoUrn-')]")
            _locations: List[str] = [label.find_element_by_tag_name(
                "span").text for label in _location_labels]
            del _location_labels
            _locations_dict: Dict[str, webdriver.Chrome]
            for _location, _location_inp in zip(_locations, _location_inps):
                _locations_dict[_location] = _location_inp
            del _locations
            del _location_inps

            check_for_filter(self._location, _locations_dict)
            del _locations_dict

        if self._industry:
            _industry_inps: webdriver.Chrome = get_elements_by_xpath(
                "//input[starts-with(@id, 'advanced-filter-industry-')]")
            _industry_labels: webdriver.Chrome = get_elements_by_xpath(
                "//label[starts-with(@for, 'advanced-filter-industry-')]")
            _industries: List[str] = [label.find_element_by_tag_name(
                "span").text for label in _industry_labels]
            del _industry_labels
            _industries_dict: Dict[str, webdriver.Chrome]
            for _industry, _industry_inp in zip(_industries, _industry_inps):
                _industries_dict[_industry] = _industry_inp
            del _industries
            del _industry_inps

            check_for_filter(self._industry, _industries_dict)
            del _industries_dict

        if self._profile_language:
            _profile_language_inps: webdriver.Chrome = get_elements_by_xpath(
                "//input[starts-with(@id, 'advanced-filter-profileLanguage-')]")
            _profile_language_labels: webdriver.Chrome = get_elements_by_xpath(
                "//label[starts-with(@for, 'advanced-filter-profileLanguage-')]")
            _profile_languages: List[str] = [label.find_element_by_tag_name(
                "span").text for label in _profile_language_labels]
            del _profile_language_labels
            _profile_languages_dict: Dict[str, webdriver.Chrome]
            for _profile_language, _profile_language_inp in zip(_profile_languages, _profile_language_inps):
                _profile_languages_dict[_profile_language] = _profile_language_inp
            del _profile_languages
            del _profile_language_inps

            check_for_filter(self._profile_language, _profile_languages_dict)
            del _profile_languages_dict

        if self._first_name:
            _first_name_box: webdriver.Chrome = get_elements_by_xpath(
                "//label[contains(text(), 'First name')]").find_element_by_tag_name("input")
            _first_name_box.clear()
            _first_name_box.send_keys(self._first_name)
            del _first_name_box

        if self._last_name:
            _last_name_box: webdriver.Chrome = get_element_by_xpath(
                "//label[contains(text(), 'Last name')]").find_element_by_tag_name("input")
            _last_name_box.clear()
            _last_name_box.send_keys(self._last_name)
            del _last_name_box

        if self._title:
            _title_box: webdriver.Chrome = get_element_by_xpath(
                "//label[contains(text(), 'Title')]").find_element_by_tag_name("input")
            _title_box.clear()
            _title_box.send_keys(self._title)
            del _title_box

        if self._current_company:
            _company_box: webdriver.Chrome = get_element_by_xpath(
                "//label[contains(text(), 'Company')]").find_element_by_tag_name("input")
            _company_box.clear()
            _company_box.send_keys(self._current_company)
            del _company_box

        if self._school:
            _school_box: webdriver.Chrome = get_element_by_xpath(
                "//label[contains(text(), 'School')]").find_element_by_tag_name("input")
            _school_box.clear()
            _school_box.send_keys(self._school)
            del _school_box

        if self._location or self._industry or self._profile_language or self._first_name or \
                self._last_name or self._title or self._current_company or self._school:
            _show_results_button: webdriver.Chrome = get_element_by_xpath(
                "//div[@id='artdeco-modal-outlet']//button[@aria-label='Apply current filters to show results']")
            _show_results_button.click()
            del _show_results_button

    def __send_invitation(self: LinkedInSearchConnect) -> None:
        _start = time.time()

        _p = Person(self._driver)
        _persons = _p.get_search_results_elements()

        while True:
            for _person in _persons:
                if LinkedInSearchConnect.__INVITATION_SENT == self._limit:
                    break
                if _person._connect_button.text == "Pending" or \
                        _person._connect_button.get_attribute("aria-label") == "Follow":
                    continue

                try:
                    ActionChains(self._driver).move_to_element(
                        _person._connect_button).click().perform()
                    send_invite_modal = WebDriverWait(self._driver, LinkedInSearchConnect.WAIT).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@aria-labelledby='send-invite-modal']")
                        )
                    )
                    send_now = send_invite_modal.find_element_by_xpath("//button[@aria-label='Send now']")
                    ActionChains(self._driver).move_to_element(
                        send_now).click().perform()
                    Invitation(name=_person._name,
                               occupation=_person._occupation,
                               status="sent",
                               elapsed_time=time.time() - _start).status()
                    LinkedInSearchConnect.__INVITATION_SENT += 1
                except (ElementNotInteractableException,
                        ElementClickInterceptedException) as exc:
                    if isinstance(exc, ElementClickInterceptedException):
                        break
                    Invitation(name=_person._name,
                               occupation=_person._occupation,
                               status="failed",
                               elapsed_time=time.time() - _start).status()

            _next: webdriver.Chrome = self._driver.find_element_by_xpath(
                "//main[@id='main']//button[@aria-label='Next']")
            _next.click()

            _persons = _p.get_search_results_elements()

    def run(self: LinkedInSearchConnect) -> None:
        """Method run() calls the send_invitation method, but first it assures that the object
        self has driver property in it.

        :Args:
            - self: {LinkedInConnectionsAuto} object

        :Returns:
            - {None}
        """
        self.__get_search_results_page()
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

        if isinstance(self._driver, webdriver.Chrome):
            self._driver.quit()

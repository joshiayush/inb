# pylint: disable=missing-module-docstring

# Copyright 2021, joshiayus Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of joshiayus Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import re
import sys
import time
import logging
import traceback
import functools

from typing import (
    List,
    Dict,
)

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.remote import webelement
from selenium.webdriver.common import (
    by,
    keys,
    action_chains,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from linkedin import (message, driver, settings)
from linkedin.DOM import javascript
from linkedin.invitation import status

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='a')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)


class _ElementsPathSelectors:
  """Serves elements path selectors needed for scraping users information from
  the search results page.
  """

  @staticmethod
  def get_global_nav_typeahead_input_box_xpath() -> str:
    """Global nav typeahead input box `xpath`.

    Element present at this xpath lets you type in a keyword and the searches
    for people on LinkedIn that matches that keyword.

    Returns:
      Global nav typeahead input box `xpath`.
    """
    return '//*[@id="global-nav-typeahead"]/input'

  @staticmethod
  def get_filter_by_people_button_xpath() -> str:
    """Filter by people button `xpath`.

    Button present at this xpath lets you filter down the results that matches
    the keyword you typed in to only LinkedIn's `users` and removes all the
    `pages`, `jobs`, `services`, `groups`, `posts`, `courses` and `schools` that
    matches that keyword.

    Returns:
      Filter by people button `xpath`.
    """
    return '//div[@id="search-reusables__filters-bar"]//button[@aria-label="People"]'  # pylint: disable=line-too-long

  @staticmethod
  def get_all_filters_button_xpath() -> str:
    """All filters button `xpath`.

    Button present at this xpath lets you add more filters to your search
    results.  It lets you filter down your search results by the
    `connection degree`, `location`, `current company`, `past company`,
    `school`, `industry`, `profile langauge`, `service categories` and
    `keywords` related to `first name`, `last name`, `title`, `compnay`, and
    `school`.

    Returns:
      All filters button `xpath`.
    """
    return '//div[@id="search-reusables__filters-bar"]//button[@aria-label="All filters"]'  # pylint: disable=line-too-long

  @staticmethod
  def get_available_location_options_xpath() -> str:
    """Regexp `xpath` for available location options on the `filters` frame.

    This `xpath` contains regex expression so all the elements that matches this
    `xpath` will be returned in case you use this `xpath` with
    `driver.find_elements_by_xpath()` method.  This expression is used to select
    various checkboxes avialable for location filter on the `filters` frame.

    Returns:
      Regexp `xpath` for available location options on the `filters` frame.
    """
    return '//input[starts-with(@id, "advanced-filter-geoUrn-")]'

  @staticmethod
  def get_available_location_labels_xpath() -> str:
    """Regexp `xpath` for available location labels on the `filters` frame.

    This `xpath` contains regex expression so all the elements that matches this
    `xpath` will be returned in case you use this `xpath` with
    `driver.find_elements_by_xpath()` method.  This expression is used to select
    various avialable location labels on the `filters` frame.

    Returns:
      Regexp `xpath` for available location labels on the `filters` frame.
    """
    return '//label[starts-with(@for, "advanced-filter-geoUrn-")]'

  @staticmethod
  def get_available_industry_options_xpath() -> str:
    """Regexp `xpath` for available industry options on the `filters` frame.

    This `xpath` contains regex expression so all the elements that matches this
    `xpath` will be returned in case you use this `xpath` with
    `driver.find_elements_by_xpath()` method.  This expression is used to select
    various checkboxes avialable for industry filter on the `filters` frame.

    Returns:
      Regexp `xpath` for available industry options on the `filters` frame.
    """
    return '//input[starts-with(@id, "advanced-filter-industry-")]'

  @staticmethod
  def get_available_industry_labels_xpath() -> str:
    """Regexp `xpath` for available industry labels on the `filters` frame.

    This `xpath` contains regex expression so all the elements that matches this
    `xpath` will be returned in case you use this `xpath` with
    `driver.find_elements_by_xpath()` method.  This expression is used to select
    various avialable industry labels on the `filters` frame.

    Returns:
      Regexp `xpath` for available industry labels on the `filters` frame.
    """
    return '//label[starts-with(@for, "advanced-filter-industry-")]'

  @staticmethod
  def get_available_profile_language_options_xpath() -> str:
    """Regexp `xpath` for available profile language options on the `filters`
    frame.

    This `xpath` contains regex expression so all the elements that matches this
    `xpath` will be returned in case you use this `xpath` with
    `driver.find_elements_by_xpath()` method.  This expression is used to select
    various checkboxes avialable for profile language filter on the `filters`
    frame.

    Returns:
      Regexp `xpath` for available profile language options on the `filters`
        frame.
    """
    return '//input[starts-with(@id, "advanced-filter-profileLanguage-")]'

  @staticmethod
  def get_available_profile_langauge_labels_xpath() -> str:
    """Regexp `xpath` for available profile language labels on the `filters`
    frame.

    This `xpath` contains regex expression so all the elements that matches this
    `xpath` will be returned in case you use this `xpath` with
    `driver.find_elements_by_xpath()` method.  This expression is used to select
    various checkboxes avialable profile language labels on the `filters` frame.

    Returns:
      Regexp `xpath` for available profile language labels on the `filters`
        frame.
    """
    return '//label[starts-with(@for, "advanced-filter-profileLanguage-")]'

  @staticmethod
  def get_first_name_input_element_container_xpath() -> str:
    """Regexp `xpath` for the first name input element on the `filters` page.

    Input element present that matches this `xpath` is used to enter the first
    name of the person you want to search for.

    Returns:
      Regexp `xpath` for the first name input element on the `filters` page.
    """
    return '//label[contains(text(), "First name")]'

  @staticmethod
  def get_last_name_input_element_container_xpath() -> str:
    """Regexp `xpath` for the last name input element on the `filters` page.

    Input element present that matches this `xpath` is used to enter the last
    name of the person you want to search for.

    Returns:
      Regexp `xpath` for the last name input element on the `filters` page.
    """
    return '//label[contains(text(), "Last name")]'

  @staticmethod
  def get_title_input_element_container_xpath() -> str:
    """Regexp `xpath` for the title input element on the `filters` page.

    Input element present that matches this `xpath` is used to enter the title
    of the person you want to search for.

    Returns:
      Regexp `xpath` for the title input element on the `filters` page.
    """
    return '//label[contains(text(), "Title")]'

  @staticmethod
  def get_current_company_input_element_container_xpath() -> str:
    """Regexp `xpath` for the current company input element on the `filters`
    page.

    Input element present that matches this `xpath` is used to enter the current
    company of the person you want to search for.

    Returns:
      Regexp `xpath` for the current company input element on the `filters`
        page.
    """
    return '//label[contains(text(), "Company")]'

  @staticmethod
  def get_school_input_element_container_xpath() -> str:
    """Regexp `xpath` for the school input element on the `filters` page.

    Input element present that matches this `xpath` is used to enter the school
    the person you want to search for.

    Returns:
      Regexp `xpath` for the school input element on the `filters` page.
    """
    return '//label[contains(text(), "School")]'

  @staticmethod
  def get_apply_current_filters_button_xpath() -> str:
    """Apply current filters button `xpath`.

    Button present at this `xpath` is used to apply the filters program has
    selected so far.

    Returns:
      Apply current filters button `xpath`.
    """
    return '//div[@id="artdeco-modal-outlet"]//button[@aria-label="Apply current filters to show results"]'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_parent_xpath() -> str:
    """Person `li` element's parent element i.e., `ul`.

    This is the parent element that contains all the `li` tags for LinkedIn
    users.

    Returns:
      Person `li` element's parent element i.e., `ul`.
    """
    return '//*[@id="main"]/div/div/div[2]/ul'

  @staticmethod
  def get_search_results_person_li_xpath(positiion: int) -> str:
    """Search results person `li` xpath located at `position`.

    This function returns the `li` tag inside the parent `ul` tag located at
    `position` that contains the information of a LinkedIn user.

    Args:
      position: `li` position.

    Returns:
      Search results person `li` xpath located at `position`.
    """
    return f'{_ElementsPathSelectors.get_search_results_person_li_parent_xpath()}/li[{positiion}]'  # pylint: disable=line-too-long

  @staticmethod
  def _get_search_results_person_li_card_container_xpath(position: int) -> str:
    """`xpath` for person's card container.

    This function returns the card container of an `li` tag located at
    `position` inside the `ul` parent element.

    Args:
      position: `li` position.

    Returns:
      `xpath` for person's card container.
    """
    return f'{_ElementsPathSelectors.get_search_results_person_li_xpath(position)}/div/div'  # pylint: disable=line-too-long

  @staticmethod
  def _get_search_results_person_li_card_info_container_xpath(
      position: int) -> str:
    """`xpath` for person's information card container.

    This function returns `xpath` for parent element that contains the person's
    information located at `position`.

    Returns:
      `xpath` for person's information card container.
    """
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_container_xpath(position)}/div[2]'  # pylint: disable=line-too-long

  @staticmethod
  def _get_search_results_person_li_card_info_nav_xpath(position: int) -> str:
    """`xpath` to person card information nav bar.

    Element at this `xpath` is a container that contains the person name and
    the connection degree information.

    Args:
      position: `li` position.

    Returns:
      `xpath` to person card information nav bar.
    """
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_info_container_xpath(position)}/div[1]/div[1]/div'  # pylint: disable=line-too-long

  @staticmethod
  def _get_search_results_person_li_card_info_footer_xpath(
      position: int) -> str:
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_info_container_xpath(position)}/div[2]'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_card_mutual_connections_info_container_xpath(
      position: int) -> str:
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_info_footer_xpath(position)}/div/div[2]/span'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_card_link_xpath(position: int) -> str:
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_info_nav_xpath(position)}/span[1]/span/a'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_card_name_xpath(position: int) -> str:
    """`xpath` to the direct element that contains person name.

    This element is a direct container element that contains person name that
    is located at `position` inside `ul`.

    Args:
      position: `li` position.

    Returns:
      `xpath` to the direct element that contains person name.
    """
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_info_nav_xpath(position)}/span[1]/span/a/span/span[1]'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_card_degree_info_xpath(position: int) -> str:
    """`xpath` to the direct element that contains degree of connection that
    person is with you.

    This element is a direct container element that contains the degree of
    connection that person is with you that is located at `position` inside
    `ul`.

    Args:
      position: `li` position.

    Returns:
      `xpath` to the direct element that contains degree of connection that
        person is with you.
    """
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_info_nav_xpath(position)}/span[2]/div/span/span[2]'  # pylint: disable=line-too-long

  @staticmethod
  def _get_search_results_person_li_occupation_and_location_info_card_container_xpath(  # pylint: disable=line-too-long
      position: int) -> str:
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_info_container_xpath(position)}/div[1]/div[2]'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_occupation_info_card_container_xpath(
      position: int) -> str:
    return f'{_ElementsPathSelectors._get_search_results_person_li_occupation_and_location_info_card_container_xpath(position)}/div/div[1]'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_location_info_card_container_xpath(
      position: int) -> str:
    return f'{_ElementsPathSelectors._get_search_results_person_li_occupation_and_location_info_card_container_xpath(position)}/div/div[2]'  # pylint: disable=line-too-long

  @staticmethod
  def _get_search_results_person_li_card_actions_container_xpath(
      position: int) -> str:
    """`xpath` to the actions container of the person `li` at `position`.

    Element located at this `xpath` is the parent element for the connect
    button.

    Args:
      position: `li` position.

    Returns:
      `xpath` to the actions container of the person `li` at `position`.
    """
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_container_xpath(position)}/div[3]'  # pylint: disable=line-too-long

  @staticmethod
  def get_search_results_person_li_connect_button_xpath(position: int) -> str:
    """`xpath` to the person connect button.

    Args:
      position: `li` position.

    Returns:
      `xpath` to the person connect button.
    """
    return f'{_ElementsPathSelectors._get_search_results_person_li_card_actions_container_xpath(position)}/button'  # pylint: disable=line-too-long

  @staticmethod
  def get_send_invite_modal_xpath() -> str:
    """"""
    return '//div[@aria-labelledby="send-invite-modal"]'

  @staticmethod
  def get_send_now_button_xpath() -> str:
    """"""
    return '//button[@aria-label="Send now"]'

  @staticmethod
  def get_goto_next_page_button_xpath() -> str:
    """"""
    return '//main[@id="main"]//button[@aria-label="Next"]'


class _Person:

  def __init__(self, name: str, degree: str, occupation: str, location: str,
               mutual_connections: str, profileid: str, profileurl: str,
               connect_button: webelement.WebElement):
    self.name = name
    self.degree = degree
    self.occupation = occupation
    self.location = location
    self.mutual_connections = mutual_connections
    self.profileid = profileid
    self.profileurl = profileurl
    self.connect_button = connect_button

  @staticmethod
  def extract_profileid_from_profileurl(profileurl: str) -> str:
    re_ = re.compile(r'([a-z]+-?)+([a-zA-Z0-9]+)?', re.IGNORECASE)
    return re_.search(profileurl).group(0)


def _GetElementByXPath(xpath: str, wait: int = 60) -> webelement.WebElement:
  while True:
    try:
      return WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
          EC.presence_of_element_located((by.By.XPATH, xpath)))
    except (exceptions.TimeoutException,
            exceptions.NoSuchElementException) as error:
      logger.error(traceback.format_exc())
      if isinstance(error, exceptions.TimeoutException):
        javascript.JS.load_page()
      continue


def _GetLiElementsFromPage(wait: int = 60) -> List[webelement.WebElement]:
  return _GetElementByXPath(
      _ElementsPathSelectors.get_search_results_person_li_parent_xpath(),
      wait).find_elements_by_tag_name('li')


_LINKEDIN_MAX_INVITATION_LIMIT = 80


def _GetSearchResultsPersonLiObjects() -> List[_Person]:
  person_li_count = 0
  while True:
    for i in range(len(_GetLiElementsFromPage())):
      name = _GetElementByXPath(
          _ElementsPathSelectors.get_search_results_person_li_card_name_xpath(
              i + 1)).text
      degree = _GetElementByXPath(
          _ElementsPathSelectors.
          get_search_results_person_li_card_degree_info_xpath(i + 1)).text
      occupation = _GetElementByXPath(
          _ElementsPathSelectors.
          get_search_results_person_li_occupation_info_card_container_xpath(
              i + 1)).text
      location = _GetElementByXPath(
          _ElementsPathSelectors.
          get_search_results_person_li_location_info_card_container_xpath(
              i + 1)).text
      mutual_connections = _GetElementByXPath(
          _ElementsPathSelectors.
          get_search_results_person_li_card_mutual_connections_info_container_xpath(  # pylint: disable=line-too-long
              i + 1)).text
      profileurl = _GetElementByXPath(
          _ElementsPathSelectors.get_search_results_person_li_card_link_xpath(
              i + 1)).get_attribute('href')
      connect_button = _GetElementByXPath(
          _ElementsPathSelectors.
          get_search_results_person_li_connect_button_xpath(i + 1))
      yield _Person(name, degree, occupation, location, mutual_connections,
                    _Person.extract_profileid_from_profileurl(profileurl),
                    profileurl, connect_button)
      person_li_count += 1

    if person_li_count == _LINKEDIN_MAX_INVITATION_LIMIT:
      return

    def goto_next_page() -> None:  # pylint: disable=redefined-builtin
      next_button = driver.GetGlobalChromeDriverInstance(
      ).find_element_by_xpath(
          _ElementsPathSelectors.get_goto_next_page_button_xpath())
      action_chains.ActionChains(
          driver.GetGlobalChromeDriverInstance()).move_to_element(
              next_button).click().perform()

    try:
      goto_next_page()
    except exceptions.NoSuchElementException:
      javascript.JS.load_page()
      goto_next_page()


class LinkedInSearchConnect:

  def __init__(self, *, keyword: str, location: str, title: str, firstname: str,
               lastname: str, school: str, industry: str, current_company: str,
               profile_language: str, max_connection_limit: int) -> None:
    if max_connection_limit is None:
      max_connection_limit = 20
    elif not 0 < max_connection_limit <= 80:
      raise ValueError(settings.CONNECTION_LIMIT_EXCEED_EXCEPTION_MESSAGE %
                       (max_connection_limit))
    self._max_connection_limit = max_connection_limit

    if keyword is None:
      raise ValueError(
          "Function expects at least one argument 'keyword'. Provide a industry"
          " keyword such as 'Software Developer', 'Hacker' or you can pass in"
          " someone's name like 'Mohika' you want to connect with.")
    self._keyword = keyword
    self._location = location
    self._title = title
    self._firstname = firstname
    self._lastname = lastname
    self._school = school
    self._industry = industry
    self._current_company = current_company
    self._profile_language = profile_language

  def _get_search_results_page(self) -> None:
    typeahead_input_box = self._get_element_by_xpath(
        _ElementsPathSelectors.get_global_nav_typeahead_input_box_xpath())
    try:
      typeahead_input_box.clear()
    except exceptions.InvalidElementStateException:
      logger.error(traceback.format_exc())
    typeahead_input_box.send_keys(self._keyword)
    typeahead_input_box.send_keys(keys.Keys.RETURN)

  def _get_element_by_xpath(self,
                            xpath: str,
                            wait: int = 60) -> webdriver.Chrome:
    return WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
        EC.presence_of_element_located((by.By.XPATH, xpath)))

  def _get_elements_by_xpath(self,
                             xpath: str,
                             wait: int = 60) -> webdriver.Chrome:
    return WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
        EC.presence_of_all_elements_located((by.By.XPATH, xpath)))

  def _check_if_any_filter_is_given(self) -> bool:
    return any([
        self._location, self._industry, self._profile_language, self._firstname,
        self._lastname, self._title, self._current_company, self._school
    ])

  def _apply_filters_to_search_results(self):
    filter_by_people_button = self._get_element_by_xpath(
        _ElementsPathSelectors.get_filter_by_people_button_xpath())
    filter_by_people_button.click()
    del filter_by_people_button

    if self._check_if_any_filter_is_given():
      all_filters_button = self._get_element_by_xpath(
          _ElementsPathSelectors.get_all_filters_button_xpath())
      all_filters_button.click()
      del all_filters_button

    def check_for_filter(
        filter: str,  # pylint: disable=redefined-builtin
        filter_dict: Dict[str, webdriver.Chrome]
    ) -> None:
      nonlocal self
      filters_present: List[str] = filter_dict.keys()

      def click_overlapped_element(element: webdriver.Chrome) -> None:
        """Nested function click_overlapped_element() fixes the WebdriverException:
        Element is not clickable at point (..., ...).

        :Args:
            - element: {webdriver.Chrome} Element.
        """
        nonlocal self
        # @TODO: Validate if the current version of this function is efficient
        driver.GetGlobalChromeDriverInstance().execute_script(
            'arguments[0].click();', element)

      if isinstance(filter, str):
        if filter in filters_present:
          click_overlapped_element(filter_dict[filter])
        else:
          raise RuntimeError('Given filter "' + filter + '" is not present.')
        return

      if isinstance(filter, list):
        for fltr in filter:
          if fltr in filters_present:
            click_overlapped_element(filter_dict[fltr])
            continue
          else:
            raise RuntimeError('Given filter "' + fltr + '" is not present.')
        return

    if self._location:
      available_location_options = self._get_elements_by_xpath(
          _ElementsPathSelectors.get_available_location_options_xpath())
      available_location_labels = self._get_elements_by_xpath(
          _ElementsPathSelectors.get_available_location_labels_xpath())
      available_locations: List[str] = [
          label.find_element_by_tag_name('span').text
          for label in available_location_labels
      ]

      del available_location_labels
      locations_dict: Dict[str, webdriver.Chrome] = {}
      for location, location_option in zip(available_locations,
                                           available_location_options):
        locations_dict[location] = location_option
      del available_locations
      del available_location_options

      check_for_filter(self._location, locations_dict)
      del locations_dict

    if self._industry:
      available_industry_options = self._get_elements_by_xpath(
          _ElementsPathSelectors.get_available_industry_options_xpath())
      available_industry_labels = self._get_elements_by_xpath(
          _ElementsPathSelectors.get_available_industry_labels_xpath())
      available_industries: List[str] = [
          label.find_element_by_tag_name('span').text
          for label in available_industry_labels
      ]

      del available_industry_labels
      industries_dict: Dict[str, webdriver.Chrome] = {}
      for industry, industry_option in zip(available_industries,
                                           available_industry_options):
        industries_dict[industry] = industry_option
      del available_industries
      del available_industry_options

      check_for_filter(self._industry, industries_dict)
      del industries_dict

    if self._profile_language:
      available_profile_language_options = self._get_elements_by_xpath(
          _ElementsPathSelectors.get_available_profile_language_options_xpath())
      available_profile_language_lables = self._get_elements_by_xpath(
          _ElementsPathSelectors.get_available_profile_langauge_labels_xpath())
      available_profile_languages: List[str] = [
          label.find_element_by_tag_name('span').text
          for label in available_profile_language_lables
      ]

      del available_profile_language_lables
      profile_languages_dict: Dict[str, webdriver.Chrome] = {}
      for profile_language, profile_language_option in zip(
          available_profile_languages, available_profile_language_options):
        profile_languages_dict[profile_language] = profile_language_option
      del available_profile_languages
      del available_profile_language_options

      check_for_filter(self._profile_language, profile_languages_dict)
      del profile_languages_dict

    if self._firstname:
      firstname_input_element = self._get_elements_by_xpath(
          _ElementsPathSelectors.get_first_name_input_element_container_xpath(
          )).find_element_by_tag_name('input')
      firstname_input_element.clear()
      firstname_input_element.send_keys(self._firstname)
      del firstname_input_element

    if self._lastname:
      lastname_input_element = self._get_element_by_xpath(
          _ElementsPathSelectors.get_last_name_input_element_container_xpath(
          )).find_element_by_tag_name('input')
      lastname_input_element.clear()
      lastname_input_element.send_keys(self._lastname)
      del lastname_input_element

    if self._title:
      title_input_element = self._get_element_by_xpath(
          _ElementsPathSelectors.get_title_input_element_container_xpath(
          )).find_element_by_tag_name('input')
      title_input_element.clear()
      title_input_element.send_keys(self._title)
      del title_input_element

    if self._current_company:
      current_company_input_element = self._get_element_by_xpath(
          _ElementsPathSelectors.
          get_current_company_input_element_container_xpath(
          )).find_element_by_tag_name('input')
      current_company_input_element.clear()
      current_company_input_element.send_keys(self._current_company)
      del current_company_input_element

    if self._school:
      school_input_element = self._get_element_by_xpath(
          _ElementsPathSelectors.get_school_input_element_container_xpath(
          )).find_element_by_tag_name('input')
      school_input_element.clear()
      school_input_element.send_keys(self._school)
      del school_input_element

    if self._check_if_any_filter_is_given():
      apply_current_filters_button = self._get_element_by_xpath(
          _ElementsPathSelectors.get_apply_current_filters_button_xpath())
      apply_current_filters_button.click()
      del apply_current_filters_button

  def _search_and_filter_results(function_: function):  # pylint: disable=undefined-variable, no-self-argument

    @functools.wraps(function_)
    def wrapper(self, *args, **kwargs):
      self._get_search_results_page()  # pylint: disable=protected-access
      self._apply_filters_to_search_results()  # pylint: disable=protected-access
      function_(*args, **kwargs)  # pylint: disable=not-callable

    return wrapper

  @_search_and_filter_results
  def send_connection_request(self) -> None:
    invitation_count = 0
    start_time = time.time()

    invitation = status.Invitation()
    for person in _GetSearchResultsPersonLiObjects():
      if (person.connect_button.text == 'Pending' or
          person.connect_button.get_attribute('aria-label')
          in ('Follow', 'Message')):
        continue
      try:
        action_chains.ActionChains(
            driver.GetGlobalChromeDriverInstance()).move_to_element(
                person.connect_button).click().perform()
        send_now_button = self._get_element_by_xpath(
            _ElementsPathSelectors.get_send_invite_modal_xpath(
            )).find_element_by_xpath(
                _ElementsPathSelectors.get_send_now_button_xpath())
        action_chains.ActionChains(
            driver.GetGlobalChromeDriverInstance()).move_to_element(
                send_now_button).click().perform()
        invitation.display_invitation_status_on_console(person, 'sent',
                                                        start_time)
        invitation_count += 1
      except (exceptions.ElementNotInteractableException,
              exceptions.ElementClickInterceptedException) as exc:
        logger.error(traceback.format_exc())
        if isinstance(exc, exceptions.ElementClickInterceptedException):
          break
        invitation.display_invitation_status_on_console(person, 'failed',
                                                        start_time)

      if invitation_count == self._max_connection_limit:
        break

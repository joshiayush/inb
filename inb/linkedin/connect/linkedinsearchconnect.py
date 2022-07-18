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

from typing import Optional

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

from linkedin import (driver, settings)
from linkedin.DOM import javascript
from linkedin.message import template
from linkedin.connect import pathselectorbuilder
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
  """Serves elements' path selectors needed for scraping users information from
  the search results page.
  """

  @staticmethod
  def get_global_nav_typeahead_input_box_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the global nav typeahead input box.

    Returns:
      The path selector for the global nav typeahead input box and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Global <nav> typeahead input box',
        '//*[@id="global-nav-typeahead"]/input')

  @staticmethod
  def get_filter_by_people_button_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the filter by people button.

    Returns:
      The path selector for the filter by people button and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Filter by people button',
        '//div[@id="search-reusables__filters-bar"]//button[@aria-label="People"]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_all_filters_button_xpath() -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the all filters button.

    Returns:
      The path selector for the all filters button and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'All filters button',
        '//div[@id="search-reusables__filters-bar"]//button[starts-with(@aria-label, "Show all filters.")]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_available_location_options_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the available location options.

    Returns:
      The path selector for the available location options and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Available location options',
        '//input[starts-with(@id, "advanced-filter-geoUrn-")]')

  @staticmethod
  def get_available_location_labels_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the available location labels.

    Returns:
      The path selector for the available location labels and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Available location labels',
        '//label[starts-with(@for, "advanced-filter-geoUrn-")]')

  @staticmethod
  def get_available_industry_options_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the available industry options.

    Returns:
      The path selector for the available industry options and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Available industry options',
        '//input[starts-with(@id, "advanced-filter-industry-")]')

  @staticmethod
  def get_available_industry_labels_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the available industry labels.

    Returns:
      The path selector for the available industry labels and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Available industry labels',
        '//label[starts-with(@for, "advanced-filter-industry-")]')

  @staticmethod
  def get_available_profile_language_options_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the available profile language options.

    Returns:
      The path selector for the available profile language options and its
      label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Available profile language options',
        '//input[starts-with(@id, "advanced-filter-profileLanguage-")]')

  @staticmethod
  def get_available_profile_langauge_labels_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the available profile language labels.

    Returns:
      The path selector for the available profile language labels and its
      label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Available profile language labels',
        '//label[starts-with(@for, "advanced-filter-profileLanguage-")]')

  @staticmethod
  def get_first_name_input_element_container_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the first name input element container.

    Returns:
      The path selector for the first name input element container and its
      label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'First name <input> element container',
        '//label[contains(text(), "First name")]')

  @staticmethod
  def get_last_name_input_element_container_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the last name input element container.

    Returns:
      The path selector for the last name input element container and its
      label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Last name <input> element container',
        '//label[contains(text(), "Last name")]')

  @staticmethod
  def get_title_input_element_container_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the title input element container.

    Returns:
      The path selector for the title input element container and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Title <input> element container', '//label[contains(text(), "Title")]')

  @staticmethod
  def get_current_company_input_element_container_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the current company input element
    container.

    Returns:
      The path selector for the current company input element container and
      its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Current company <input> element container',
        '//label[contains(text(), "Company")]')

  @staticmethod
  def get_school_input_element_container_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the school input element container.

    Returns:
      The path selector for the school input element container and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'School <input> element container',
        '//label[contains(text(), "School")]')

  @staticmethod
  def get_apply_current_filters_button_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the apply current filters button.

    Returns:
      The path selector for the apply current filters button and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Apply current filters <button>',
        '//div[@id="artdeco-modal-outlet"]//button[@aria-label="Apply current filters to show results"]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_parent_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li parent.

    Returns:
      The path selector for the search results person li parent and its
      label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> parent',
        '//*[@id="main"]/div/div/div[1]/ul')

  @staticmethod
  def get_search_results_person_li_xpath(
      positiion: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li>',
        f'{_ElementsPathSelectors.get_search_results_person_li_parent_xpath()}/li[{positiion}]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def _get_search_results_person_li_card_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    container.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card container and
      its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card container',
        f'{_ElementsPathSelectors.get_search_results_person_li_xpath(position)}/div/div'  # pylint: disable=line-too-long
    )

  @staticmethod
  def _get_search_results_person_li_card_info_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    info container.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card info container
      and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card info container',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_container_xpath(position)}/div[2]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def _get_search_results_person_li_card_info_nav_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    info nav.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card info nav and
      its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card info <nav>',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_info_container_xpath(position)}/div[1]/div[1]/div'  # pylint: disable=line-too-long
    )

  @staticmethod
  def _get_search_results_person_li_card_info_footer_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    info footer.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card info footer
      and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card info <footer>',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_info_container_xpath(position)}/div[3]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_card_mutual_connections_info_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    mutual connections info container.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card mutual
      connections info container and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card mutual connections info container',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_info_footer_xpath(position)}/div/div[2]/span'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_card_link_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    link.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card link and
      its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card link',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_info_nav_xpath(position)}/span[1]/span/a'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_card_name_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    name.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card name and
      its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card name',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_info_nav_xpath(position)}/span[1]/span/a/span/span[1]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_card_degree_info_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    degree info.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card degree info
      and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card degree info',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_info_nav_xpath(position)}/span[2]/div/span/span[2]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def _get_search_results_person_li_occupation_and_location_info_card_container_xpath(  # pylint: disable=line-too-long
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li occupation
    and location info card container.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li occupation and
      location info card container and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> occupation and location info card container',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_info_container_xpath(position)}/div[1]/div[2]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_occupation_info_card_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li occupation
    info card container.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li occupation info
      card container and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> occupation info card container',
        f'{_ElementsPathSelectors._get_search_results_person_li_occupation_and_location_info_card_container_xpath(position)}/div/div[1]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_location_info_card_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li location
    info card container.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li location info
      card container and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> location info card container',
        f'{_ElementsPathSelectors._get_search_results_person_li_occupation_and_location_info_card_container_xpath(position)}/div/div[2]'  # pylint: disable=line-too-long
    )

  @staticmethod
  def _get_search_results_person_li_card_actions_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li card
    actions container.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li card actions
      container and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> card actions container',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_container_xpath(position)}/div[3]/div'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_search_results_person_li_connect_button_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the search results person li connect
    button.

    Args:
      position: `li` position.

    Returns:
      The path selector for the search results person li connect button
      and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Search results person <li> connect button',
        f'{_ElementsPathSelectors._get_search_results_person_li_card_actions_container_xpath(position)}/button'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_send_invite_modal_xpath() -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the send invite modal.

    Returns:
      The path selector for the send invite modal and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Send invite modal', '//div[@aria-labelledby="send-invite-modal"]')

  @staticmethod
  def get_send_now_button_xpath() -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the send now button.

    Returns:
      The path selector for the send now button and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Send now <button>', '//button[@aria-label="Send now"]')

  @staticmethod
  def get_goto_next_page_button_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the path selector for the goto next page button.

    Returns:
      The path selector for the goto next page button and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Goto next page <button>',
        '//main[@id="main"]//button[@aria-label="Next"]')


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


def _GetElementByXPath(xpath: pathselectorbuilder.PathSelectorBuilder,
                       wait: int = 60) -> webelement.WebElement:
  while True:
    try:
      return WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
          EC.presence_of_element_located((by.By.XPATH, str(xpath))))
    except exceptions.TimeoutException as error:
      logger.critical('%s Element could not be found at: %s for label: %s',
                      traceback.format_exc().strip('\n').strip(), str(xpath),
                      xpath.path_label)
      if isinstance(error, exceptions.TimeoutException):
        javascript.JS.load_page()
        continue


def _GetLiElementsFromPage(wait: int = 60) -> list[webelement.WebElement]:
  return _GetElementByXPath(
      _ElementsPathSelectors.get_search_results_person_li_parent_xpath(),
      wait).find_elements_by_tag_name('li')


_LINKEDIN_MAX_INVITATION_LIMIT = 80


def _GetSearchResultsPersonLiObjects() -> list[_Person]:
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
      # @TODO(joshiayush): Some users on LinkedIn does not have information of
      # shared connections in the
      # _ElementsPathSelectors.
      #     get_search_results_person_li_card_mutual_connections_info_container_xpath(  # pylint: disable=line-too-long
      #         i + 1)).text
      # path.  To comabt this we must modify our API to quickly raise an exception
      # when this happens so that we can quickly catch it and replace the
      # `mutual_connections` variable with `'Shared connections not found :('` string.
      #
      # mutual_connections = _GetElementByXPath(
      #     _ElementsPathSelectors.
      #     get_search_results_person_li_card_mutual_connections_info_container_xpath(  # pylint: disable=line-too-long
      #         i + 1)).text
      mutual_connections = (
          "Automation using 'search' command could not scrape information of\n"
          '  shared connections properly.\n'
          '  Please be kind an send us a pull request :)')
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

  def __init__(self,
               *,
               keyword: str,
               location: str,
               title: str,
               firstname: str,
               lastname: str,
               school: str,
               industry: str,
               current_company: str,
               profile_language: str,
               max_connection_limit: int,
               template_file: Optional[str] = None) -> None:
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
    if template_file is not None:
      self._invitation_message = template.ReadTemplate(template_file)
    else:
      self._invitation_message = None

  def get_search_results_page(self) -> None:
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
        filter_dict: dict[str, webdriver.Chrome]
    ) -> None:
      nonlocal self
      filters_present: list[str] = filter_dict.keys()

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
      available_locations: list[str] = [
          label.find_element_by_tag_name('span').text
          for label in available_location_labels
      ]

      del available_location_labels
      locations_dict: dict[str, webdriver.Chrome] = {}
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
      available_industries: list[str] = [
          label.find_element_by_tag_name('span').text
          for label in available_industry_labels
      ]

      del available_industry_labels
      industries_dict: dict[str, webdriver.Chrome] = {}
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
      available_profile_languages: list[str] = [
          label.find_element_by_tag_name('span').text
          for label in available_profile_language_lables
      ]

      del available_profile_language_lables
      profile_languages_dict: dict[str, webdriver.Chrome] = {}
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

  def send_connection_requests(self) -> None:
    self._apply_filters_to_search_results()

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

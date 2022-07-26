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

"""Module `linkedinconnect.py` serves as a interface between the user and
the LinkedIn's `MyNetwork` page.  It allows the user to send invitations to
the people in the `MyNetwork` page.

The `linkedinconnect.py` module is a wrapper around the `selenium` module
and in some places it is an extension to the `selenium` module.

  * `selenium` module is used to interact with the `MyNetwork` page.

You can directly use the following class to interact with the `MyNetwork` page:

  * `LinkedInConnect`

  ```python
  # Initializing the `LinkedInConnect` class.
  linkedinconnect = connect.LinkedInConnect(max_connection_limit=limit)

  # Get the `MyNetwork` page.
  linkedinconnect.get_my_network_page()

  # Send invitation requests to people.
  linkedinconnect.send_connection_requests()
  ```

Author: Ayush Joshi <ayush854032@gmail.com>
"""

from __future__ import annotations

import sys
import time
import logging
import traceback

from selenium.common import exceptions
from selenium.webdriver.remote import webelement
from selenium.webdriver.common import action_chains

from linkedin import (driver, settings, connect)
from linkedin.document_object_module import cleaners
from linkedin.connect import (pathselectorbuilder, utils)
from linkedin.invitation import status

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='a')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)


class _MyNetworkPageElementsPathSelectors:
  """Serves elements' path selectors needed for scraping users information from
  the MyNetwork page.
  """

  @staticmethod
  def _get_suggestion_box_person_li_parent_xpath(
  ) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the parent element of the suggestion box with its
    label.

    Returns:
      A tuple of the xpath of the parent element of the suggestion box with its
      label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion box person <li> parent element',
        '/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div[2]/section/section/section/div/ul'  # pylint: disable=line-too-long
    )

  @staticmethod
  def get_suggestion_box_li_root_xpath(
      positiion: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the root element of the suggestion box and its
    label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the root element of the suggestion box and its
      label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element',
        _MyNetworkPageElementsPathSelectors.
        _get_suggestion_box_person_li_parent_xpath() + '/li[' + str(positiion) +
        ']')

  @staticmethod
  def _get_suggestion_box_li_card_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card container element of the suggestion box and
    its label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card container element of the suggestion box
      and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card container',
        _MyNetworkPageElementsPathSelectors.get_suggestion_box_li_root_xpath(
            position) + '/div/section')

  @staticmethod
  def _get_suggestion_box_li_card_info_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card info container element of the suggestion
    box and its label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card info container element of the suggestion
      box and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card info container',
        _MyNetworkPageElementsPathSelectors.
        _get_suggestion_box_li_card_container_xpath(position) + '/div[1]')

  @staticmethod
  def get_suggestion_box_li_card_link_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card link element of the suggestion box and its
    label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card link element of the suggestion box and
      its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card link container',
        _MyNetworkPageElementsPathSelectors.
        _get_suggestion_box_li_card_info_container_xpath(position) + '/a')

  @staticmethod
  def get_suggestion_box_li_card_name_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card name element of the suggestion box and its
    label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card name element of the suggestion box and
      its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card name container',
        _MyNetworkPageElementsPathSelectors.
        get_suggestion_box_li_card_link_xpath(position) + '/span[2]')

  @staticmethod
  def get_suggestion_box_li_card_occupation_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card occupation element of the suggestion
    box and its label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card occupation element of the suggestion
      box and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card occupation container',
        _MyNetworkPageElementsPathSelectors.
        get_suggestion_box_li_card_link_xpath(position) + '/span[4]')

  @staticmethod
  def _get_suggestion_box_li_card_bottom_container_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card bottom container element of the suggestion
    box and its label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card bottom container element of the
      suggestion box and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card bottom container',
        _MyNetworkPageElementsPathSelectors.
        _get_suggestion_box_li_card_container_xpath(position) + '/div[2]')

  @staticmethod
  def get_suggestion_box_li_card_member_mutual_connections_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card member mutual connections element of the
    suggestion box and its label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card member mutual connections element of
      the suggestion box and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card member mutual connections container',
        _MyNetworkPageElementsPathSelectors.
        _get_suggestion_box_li_card_bottom_container_xpath(position) +
        '/div/div/button/span')

  @staticmethod
  def get_suggestion_box_li_card_invite_button_xpath(
      position: int) -> pathselectorbuilder.PathSelectorBuilder:
    """Returns the xpath of the card invite button element of the suggestion
    box and its label.

    Args:
      position: The position of the li element.

    Returns:
      A tuple of the xpath of the card invite button element of the suggestion
      box and its label.
    """
    return pathselectorbuilder.PathSelectorBuilder(
        'Suggestion Box <li> element card invite button',
        _MyNetworkPageElementsPathSelectors.
        _get_suggestion_box_li_card_bottom_container_xpath(position) +
        '/footer/button')


class _Person:
  """A separate type for the LinkedIn user inside our program particularly
  aimed for the `LinkedInConnect` API.

  Used inside the protected function `_GetSuggestionBoxPersonLiObject()`
  after storing the person information from the `document_object_module`
  inside the local variables like you can see below:

  ```python
  def _GetSuggestionBoxPersonLiObject(position: int) -> _Person:
    ...
    return _Person(name, occupation, mutual_connections, profileid, profileurl,
                   connect_button)
  ```
  """

  def __init__(self, name: str, occupation: str, mutual_connections: str,
               profileid: str, profileurl: str,
               connect_button: webelement.WebElement):
    self.name = name
    self.occupation = occupation
    self.mutual_connections = mutual_connections

    # profileid should not be dumped into the console rather it should be put
    # inside the log records i.e., our history database.
    self.profileid = profileid

    # profileurl should not be dumped into the console rather it should be put
    # inside the log records i.e., our history database.
    self.profileurl = profileurl
    self.connect_button = connect_button


def _GetSuggestionBoxPersonLiObject() -> _Person:
  """Generator function returns a `_Person` instance by collecting a user's
  information from the `document_object_module`.

  Every time this generator function is called it increases its
  `person_li_position` value by one and collects the information of the next
  user in the `ul` list on the `document_object_module`.

  This function uses `utils.GetElementByXPath()` protected method which
  internally makes the browser to wait explicitly until the requested element
  arrives on the `document_object_module`.

  Does not raises `StopIteration` exception instead returns silently when the
  `person_li_position` count becomes equal to the global variable
  `_LINKEDIN_MAX_INVITATION_LIMIT`, the reason why `StopIteration` is not used
  is because `pylint` says not to use it rather return silently.

  `_LINKEDIN_MAX_INVITATION_LIMIT` is neccessary as LinkedIn limits the number
  of connections a non-premium account can send in a week.
  """
  # The counter for the `li` elements in the `MyNetwork` page.
  person_li_position = 1
  while True:
    profileid = utils.GetElementByXPath(
        _MyNetworkPageElementsPathSelectors.
        get_suggestion_box_li_card_link_xpath(
            person_li_position)).get_attribute('href')
    name = utils.GetElementByXPath(
        _MyNetworkPageElementsPathSelectors.
        get_suggestion_box_li_card_name_xpath(person_li_position)).text
    occupation = utils.GetElementByXPath(
        _MyNetworkPageElementsPathSelectors.
        get_suggestion_box_li_card_occupation_xpath(person_li_position)).text
    mutual_connections = utils.GetElementByXPath(
        _MyNetworkPageElementsPathSelectors.
        get_suggestion_box_li_card_member_mutual_connections_xpath(
            person_li_position)).text
    connect_button = utils.GetElementByXPath(
        _MyNetworkPageElementsPathSelectors.
        get_suggestion_box_li_card_invite_button_xpath(person_li_position))
    profileurl = settings.GetLinkedInUrl() + profileid

    # Yield the `_Person` object with the scraped data.
    yield _Person(name, occupation, mutual_connections, profileid, profileurl,
                  connect_button)

    # Stop yielding if the counter reaches the maximum invitation limit.
    if person_li_position == connect.LINKEDIN_MAX_INVITATION_LIMIT:
      return
    person_li_position += 1


class LinkedInConnect(object):
  """Interface to interact with the LinkedIn's `MyNetwork` page.

  This interface gives functions to request the `MyNetwork` page and send
  connection requests to LinkedIn users.
  """

  def __init__(self, max_connection_limit: int):
    """Initializes the instance of `LinkedinInConnect` class with the given
    `max_connection_limit`.

    The given `max_connection_limit` should be between 0 and 80 otherwise an
    exception is raised with the message
    `settings.CONNECTION_LIMIT_EXCEED_EXCEPTION_MESSAGE`.  If the argument
    `max_connection_limit` is `None` then the `self._max_connection_limit` is
    set to 20.

    Args:
      max_connection_limit:  The maximum number of connections a non-premium
                              account can send.
    """
    if max_connection_limit is None:
      max_connection_limit = 20
    elif not 0 < max_connection_limit <= 80:
      raise ValueError(settings.CONNECTION_LIMIT_EXCEED_EXCEPTION_MESSAGE %
                       (max_connection_limit))
    self._max_connection_limit = max_connection_limit

  @staticmethod
  def get_my_network_page() -> None:
    """Function sends a `GET` request to LinkedIn's `My Network` page.

    This function must be called before calling the staticmethod
    `send_connection_requests()` otherwise you'll get a
    `NoSuchElementException` thrown at you.

    This function takes you to the `My Network` page of LinkedIn where LinkedIn
    already filters out some people that matches with your account in order to
    improve user experience so we leverage that facility in our simple `send`
    routine.
    """
    driver.GetGlobalChromeDriverInstance().get(
        settings.GetLinkedInMyNetworkPageUrl())

  def send_connection_requests(self) -> None:
    """Sends connection requests to people on your `My Network` page.

    Sends connection requests to people on your `My Network` page.  Explicitly
    waits until the elements that contains user information pops themselves up
    on the page.  This explicit wait is important that we achieve using the
    `WebDriverWait` API because LinkedIn is a dynamic website and will not pop
    the elements on the page until requested.  Protected function
    `utils.GetElementByXPath()` helps finding out the elements from the
    `document_object_module` by explicitly requesting elements from the dynamic
    page by triggering a scroll down event.

    You will also see the user's information printed on the console as this
    function sends connection request on LinkedIn.  `Invitation` API handles
    the printing of the information on the console.
    """

    # Cleaning un-neccessary elements from the `document_object_module`` is
    # neccessary so to avoid `ElementNotInteractableException`.
    cleaners.Cleaner.clear_message_overlay()

    # Set invitation count to 0 before sending any invitation request.
    invitation_count = 0
    start_time = time.time()

    invitation = status.Invitation()

    # Iterate over the person elements in the `ul` list on the Suggestion Box
    # on the MyNetwork page of the document_object_module.
    for person in _GetSuggestionBoxPersonLiObject():

      # Check if the invitation count is equal to the maximum number of
      # connections a non-premium account can send.
      if invitation_count == self._max_connection_limit:
        break
      try:
        # Move to the element on the page to avoid
        # `ElementNotInteractableException`.
        action_chains.ActionChains(
            driver.GetGlobalChromeDriverInstance()).move_to_element(
                person.connect_button).click().perform()
        invitation.display_invitation_status_on_console(person, 'sent',
                                                        start_time)

        # Increment the invitation count.
        invitation_count += 1
      except (exceptions.ElementNotInteractableException,
              exceptions.ElementClickInterceptedException) as exc:
        logger.critical(traceback.format_exc())

        # If the element is not interactable or click intercepted then we
        # assume that the page is unable to send the invitation request and
        # there's a serious problem so we just break the loop.
        if isinstance(exc, exceptions.ElementClickInterceptedException):
          break
        invitation.display_invitation_status_on_console(person, 'failed',
                                                        start_time)

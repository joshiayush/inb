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

import sys
import time
import logging
import traceback

from selenium.common import exceptions
from selenium.webdriver.remote import webelement
from selenium.webdriver.common import (by, action_chains)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from linkedin import (driver, settings)
from linkedin.DOM import (cleaners, javascript)
from linkedin.invitation import status

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='w')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)


class _ElementsPathSelectors:

  @staticmethod
  def _get_suggestion_box_person_li_parent_xpath() -> str:
    return '/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div[3]/section/section/section/div/ul'  # pylint: disable=line-too-long

  @staticmethod
  def get_suggestion_box_li_root_xpath(positiion: int) -> str:
    return _ElementsPathSelectors._get_suggestion_box_person_li_parent_xpath(
    ) + '/li[' + str(positiion) + ']'

  @staticmethod
  def _get_suggestion_box_li_card_container_xpath(position: int) -> str:
    return _ElementsPathSelectors.get_suggestion_box_li_root_xpath(
        position) + '/div/section'

  @staticmethod
  def _get_suggestion_box_li_card_info_container_xpath(position: int) -> str:
    return _ElementsPathSelectors._get_suggestion_box_li_card_container_xpath(  # pylint: disable=line-too-long
        position) + '/div[1]'

  @staticmethod
  def get_suggestion_box_li_card_link_xpath(position: int) -> str:
    return _ElementsPathSelectors._get_suggestion_box_li_card_info_container_xpath(  # pylint: disable=line-too-long
        position) + '/a'

  @staticmethod
  def get_suggestion_box_li_card_name_xpath(position: int) -> str:
    return _ElementsPathSelectors.get_suggestion_box_li_card_link_xpath(
        position) + '/span[2]'

  @staticmethod
  def get_suggestion_box_li_card_occupation_xpath(position: int) -> str:
    return _ElementsPathSelectors.get_suggestion_box_li_card_link_xpath(
        position) + '/span[4]'

  @staticmethod
  def _get_suggestion_box_li_card_bottom_container_xpath(position: int) -> str:
    return _ElementsPathSelectors._get_suggestion_box_li_card_container_xpath(  # pylint: disable=line-too-long
        position) + '/div[2]'

  @staticmethod
  def get_suggestion_box_li_card_member_mutual_connections_xpath(
      position: int) -> str:
    return _ElementsPathSelectors._get_suggestion_box_li_card_bottom_container_xpath(  # pylint: disable=line-too-long
        position) + '/div/div/button/span'

  @staticmethod
  def get_suggestion_box_li_card_invite_button_xpath(position: int) -> str:  # pylint: disable=line-too-long
    return _ElementsPathSelectors._get_suggestion_box_li_card_bottom_container_xpath(  # pylint: disable=line-too-long
        position) + '/footer/button'


class _Person:
  """A separate type for the LinkedIn user inside our program particularly
  aimed for the `LinkedInConnect` API.

  Used inside the protected function `_GetSuggestionBoxPersonLiObject()`
  after storing the person information from the `DOM` inside the local
  variables like you can see below:

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
    # Note: 'profileid' and 'profileurl' should not be dumped into the console
    # rather they should be put inside the log records i.e., our history
    # database.
    self.profileid = profileid
    self.profileurl = profileurl
    self.connect_button = connect_button


def _GetElementByXPath(xpath: str, wait: int = 60) -> webelement.WebElement:
  """Returns an element from the `DOM` whose `xpath` is known.

  Function tries to find out an element from the `DOM` at the given `xpath`
  using the `WebDriverWait` API.  This function loads the page further
  immediately after the `WebDriverWait` API has raised `TimeoutException`
  in an hope that the element could be at the bottom of the page.

  THE MAIN CAVEAT here is that this function should only be used when you are
  completely sure that the element is going to reveal itself once you have
  scrolled the page a bit otherwise this function is going to stuck in an
  infinite loop and can only be stopped by the `KeyboardInterrupt` exception
  triggered explicitly.

  ```python
  # Taking the name out from the `DOM` using an explicit wait routine.
  name = _GetElementByXPath(
      _ElementsPathSelectors.get_suggestion_box_li_card_name_xpath(
          position)).text
  ```

  Args:
    xpath:  Element `xpath`.
    wait:   Time we should wait for until the element has popped itself to the
              `DOM`.

  Returns:
    `WebElement` located at the given `xpath`.
  """
  while True:
    try:
      return WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
          EC.presence_of_element_located((by.By.XPATH, xpath)))
    except exceptions.TimeoutException as exc:
      logger.critical(traceback.format_exc())
      if isinstance(exc, exceptions.TimeoutException):
        javascript.JS.load_page()
        continue


def _GetSuggestionBoxPersonLiObject(position: int) -> _Person:
  profileid = _GetElementByXPath(
      _ElementsPathSelectors.get_suggestion_box_li_card_link_xpath(
          position)).get_attribute('href')
  name = _GetElementByXPath(
      _ElementsPathSelectors.get_suggestion_box_li_card_name_xpath(
          position)).text
  occupation = _GetElementByXPath(
      _ElementsPathSelectors.get_suggestion_box_li_card_occupation_xpath(
          position)).text
  mutual_connections = _GetElementByXPath(
      _ElementsPathSelectors.
      get_suggestion_box_li_card_member_mutual_connections_xpath(position)).text
  connect_button = _GetElementByXPath(
      _ElementsPathSelectors.get_suggestion_box_li_card_invite_button_xpath(
          position))
  profileurl = settings.GetLinkedInUrl() + profileid
  return _Person(name, occupation, mutual_connections, profileid, profileurl,
                 connect_button)


class LinkedInConnect(object):

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

  @staticmethod
  def send_connection_requests(connection_limit: int = None) -> None:
    """Function sends connection requests to people on your `My Network`
    page.

    Sends connection requests to people on your `My Network` page.  Explicitly
    waits until the elements that contains user information pops themselves up
    on the page.  This explicit wait is important that we achieve using the
    `WebDriverWait` API because LinkedIn is a dynamic website and will not pop
    the elements on the page until requested.  Protected function
    `_GetElementByXPath()` helps finding out the elements from the `DOM` by
    explicitly requesting elements from the dynamic page by triggering a scroll
    down event.

    You will also see the user's information printed on the console as this
    function sends connection request on LinkedIn.  `Invitation` API handles
    the printing of the information on the console.

    Args:
      connection_limit: Number of invitations to send.  This should not exceed
                        the number 80 because LinkedIn does not allow a
                        non-premium account to send over 80 connection requests
                        in a day.
    """
    if connection_limit is None:
      connection_limit = 20
    elif not 0 < connection_limit <= 80:
      raise ValueError(settings.CONNECTION_LIMIT_EXCEED_EXCEPTION_MESSAGE %
                       (connection_limit))

    # We don't want the message overlay to overlap the 'li' tags that contains
    # the user information on your 'My Network' page as this will result in a
    # 'NoSuchElementException' if the message overlay overlaps the 'li'
    # element(s).  We remove the message overlay from the 'DOM' by setting its
    # display to 'none'.  Do you have a better idea?
    cleaners.Cleaner.clear_message_overlay()

    # We want to keep track of the invitations we've sent so far so that we can
    # later stop the connection request process once we've reached the
    # 'connection_limit'.
    invitation_count = 0
    start_time = time.time()

    invitation = status.Invitation()
    person = _GetSuggestionBoxPersonLiObject(invitation_count + 1)
    while person:
      if invitation_count == connection_limit:
        break
      try:
        action_chains.ActionChains(
            driver.GetGlobalChromeDriverInstance()).move_to_element(
                person.connect_button).click().perform()
        invitation.set_invitation_fields(
            name=person.name,
            occupation=person.occupation,
            location=None,
            mutual_connections=person.mutual_connections,
            profileid=person.profileid,
            profileurl=person.profileurl,
            status='sent',
            elapsed_time=time.time() - start_time)
        invitation.status()
        invitation_count += 1
      except (exceptions.ElementNotInteractableException,
              exceptions.ElementClickInterceptedException) as error:
        logger.critical(traceback.format_exc())
        if isinstance(error, exceptions.ElementClickInterceptedException):
          break
        invitation.set_invitation_fields(
            name=person.name,
            occupation=person.occupation,
            location=None,
            mutual_connections=person.mutual_connections,
            profileid=person.profileid,
            profileurl=person.profileurl,
            status='failed',
            elapsed_time=time.time() - start_time)
        invitation.status()
      person = _GetSuggestionBoxPersonLiObject(invitation_count + 1)

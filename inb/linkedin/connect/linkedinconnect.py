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


class SuggestionBoxPersonElements:

  @staticmethod
  def get_suggestion_box_person_li_parent() -> str:
    return '/html/body/div[6]/div[3]/div/div/div/div/div[2]/div/div/main/div[3]/section/section/section/div/ul'  # pylint: disable=line-too-long

  @staticmethod
  def get_suggestion_box_li_root_xpath(positiion: int) -> str:
    return SuggestionBoxPersonElements.get_suggestion_box_person_li_parent(
    ) + '/li[' + str(positiion) + ']'

  @staticmethod
  def _get_suggestion_box_li_card_container_xpath(position: int) -> str:
    return SuggestionBoxPersonElements.get_suggestion_box_li_root_xpath(
        position) + '/div/section'

  @staticmethod
  def _get_suggestion_box_li_card_info_container_xpath(position: int) -> str:
    return SuggestionBoxPersonElements._get_suggestion_box_li_card_container_xpath(  # pylint: disable=line-too-long
        position) + '/div[1]'

  @staticmethod
  def get_suggestion_box_li_card_link_xpath(position: int) -> str:
    return SuggestionBoxPersonElements._get_suggestion_box_li_card_info_container_xpath(  # pylint: disable=line-too-long
        position) + '/a'

  @staticmethod
  def get_suggestion_box_li_card_name_xpath(position: int) -> str:
    return SuggestionBoxPersonElements.get_suggestion_box_li_card_link_xpath(
        position) + '/span[2]'

  @staticmethod
  def get_suggestion_box_li_card_occupation_xpath(position: int) -> str:
    return SuggestionBoxPersonElements.get_suggestion_box_li_card_link_xpath(
        position) + '/span[4]'

  @staticmethod
  def _get_suggestion_box_li_card_bottom_container_xpath(position: int) -> str:
    return SuggestionBoxPersonElements._get_suggestion_box_li_card_container_xpath(  # pylint: disable=line-too-long
        position) + '/div[2]'

  @staticmethod
  def get_suggestion_box_li_card_member_mutual_connections_xpath(
      position: int) -> str:
    return SuggestionBoxPersonElements._get_suggestion_box_li_card_bottom_container_xpath(  # pylint: disable=line-too-long
        position) + '/div/div/button/span'

  @staticmethod
  def get_suggestion_box_li_card_invite_button_xpath(position: int) -> str:  # pylint: disable=line-too-long
    return SuggestionBoxPersonElements._get_suggestion_box_li_card_bottom_container_xpath(  # pylint: disable=line-too-long
        position) + '/footer/button'


class _Person:

  def __init__(self, name: str, occupation: str, mutual_connections: str,
               profileid: str, profileurl: str,
               connect_button: webelement.WebElement):
    self.name = name
    self.occupation = occupation
    self.mutual_connections = mutual_connections
    self.profileid = profileid
    self.profileurl = profileurl
    self.connect_button = connect_button


def _GetElementByXPath(xpath: str, wait: int = 60) -> webelement.WebElement:
  while True:
    try:
      return WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
          EC.presence_of_element_located((by.By.XPATH, xpath)))
    except (exceptions.TimeoutException,
            exceptions.NoSuchElementException) as error:
      logger.critical(traceback.format_exc())
      if isinstance(error, exceptions.TimeoutException):
        javascript.JS.load_page()
      continue


def _GetSuggestionBoxPersonLiObject(position: int) -> _Person:
  profileid = _GetElementByXPath(
      SuggestionBoxPersonElements.get_suggestion_box_li_card_link_xpath(
          position)).get_attribute('href')
  name = _GetElementByXPath(
      SuggestionBoxPersonElements.get_suggestion_box_li_card_name_xpath(
          position)).text
  occupation = _GetElementByXPath(
      SuggestionBoxPersonElements.get_suggestion_box_li_card_occupation_xpath(
          position)).text
  mutual_connections = _GetElementByXPath(
      SuggestionBoxPersonElements.
      get_suggestion_box_li_card_member_mutual_connections_xpath(position)).text
  connect_button = _GetElementByXPath(
      SuggestionBoxPersonElements.
      get_suggestion_box_li_card_invite_button_xpath(position))
  profileurl = settings.GetLinkedInUrl() + profileid
  return _Person(name, occupation, mutual_connections, profileid, profileurl,
                 connect_button)


class LinkedInConnect(object):

  def __init__(self, limit: int) -> None:
    assert 0 < limit <= 80, "error: inb: Limit can't be greater than 80."
    self._limit = limit
    driver.GetGlobalChromeDriverInstance().get(
        settings.GetLinkedInMyNetworkPageUrl())
    cleaners.Cleaner.clear_message_overlay()

  def send_invitations(self) -> None:
    invitation_count = 0
    start_time = time.time()

    invitation = status.Invitation()
    person = _GetSuggestionBoxPersonLiObject(invitation_count + 1)
    while person:
      if invitation_count == (self._limit - 1):
        break
      try:
        action_chains.ActionChains(
            driver.GetGlobalChromeDriverInstance()).move_to_element(
                person.connect_button).click().perform()
        invitation.set_invitation_fields(
            name=person.name,
            occupation=person.occupation,
            location=None,
            summary=None,
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
            summary=None,
            mutual_connections=person.mutual_connections,
            profileid=person.profileid,
            profileurl=person.profileurl,
            status='failed',
            elapsed_time=time.time() - start_time)
        invitation.status()
      person = _GetSuggestionBoxPersonLiObject(invitation_count + 1)

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

import os
import json
import pathlib
import unittest

from linkedin.login import login as linkedinloginroutine
from linkedin import (login, settings, driver)

from selenium.common import exceptions

_LINKEDIN_LOGIN_CREDENTIALS_FILE_PATH = pathlib.PurePath(
    __file__).parent / 'credentials.json'

if os.access(_LINKEDIN_LOGIN_CREDENTIALS_FILE_PATH, os.F_OK & os.R_OK):
  with open((pathlib.PurePath(__file__).parent / 'credentials.json'),
            encoding='UTF-8',
            mode='r') as creds_F:
    _LINKEDIN_LOGIN_CREDENTIALS = json.load(creds_F)
else:
  _LINKEDIN_LOGIN_CREDENTIALS = None


class TestLoginApiLinkedInClass(unittest.TestCase):  # pylint: disable=missing-class-docstring

  def setUp(self) -> None:
    chromedriver_options = []
    chromedriver_options.append(driver.CHROMEDRIVER_OPTIONS['headless'])
    chromedriver_options.append(driver.CHROMEDRIVER_OPTIONS['start-maximized'])
    driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsolutePath(),
                                            chromedriver_options)

  def test001_login_method_with_none_values(self) -> None:
    with self.assertRaises(ValueError):
      login.LinkedIn.login(None, None)

  def test002_linkedin_login_page_title(self) -> None:
    driver.GetGlobalChromeDriverInstance().get(
        settings.GetLinkedInLoginPageUrl())
    self.assertEqual(driver.GetGlobalChromeDriverInstance().title,
                     'LinkedIn Login, Sign in | LinkedIn')

  def test003_linkedin_login_page_signin_card(self) -> None:
    try:
      _ = driver.GetGlobalChromeDriverInstance().find_element_by_id(
          linkedinloginroutine._ElementsPathSelectors.get_username_element_id())  # pylint: disable=protected-access
    except exceptions.NoSuchElementException as exc:
      self.fail(str(exc))
    try:
      _ = driver.GetGlobalChromeDriverInstance().find_element_by_id(
          linkedinloginroutine._ElementsPathSelectors.get_password_element_id())  # pylint: disable=protected-access
    except exceptions.NoSuchElementException as exc:
      self.fail(str(exc))

  @unittest.skipIf(
      _LINKEDIN_LOGIN_CREDENTIALS is None,
      'Credentials are missing, need credentials in order to login.')
  def test004_login_method_with_valid_values(self) -> None:
    try:
      login.LinkedIn.login(_LINKEDIN_LOGIN_CREDENTIALS['username'],
                           _LINKEDIN_LOGIN_CREDENTIALS['password'])
    except exceptions.NoSuchElementException as exc:
      self.fail(str(exc))
    finally:
      driver.DisableGlobalChromeDriverInstance()

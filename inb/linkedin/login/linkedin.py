"""
This module provides service to communicate with LinkedIn's login form.

  :author: Ayush Joshi, ayush854032@gmail.com
  :copyright: Copyright (c) 2019 Creative Commons
  :license: MIT License, see license for details
"""

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

from linkedin import (driver, settings)

from selenium.webdriver.common import keys


class LoginPageElements:
  """Stores path fields of the form elements."""

  @staticmethod
  def get_username_element_name() -> str:
    return 'session_key'

  @staticmethod
  def get_password_element_name() -> str:
    return 'session_password'


class LinkedIn:
  """LinkedIn login routine."""

  @staticmethod
  def login(username: str, password: str) -> None:
    """Logs into your LinkedIn account provided that the `username` and the
    `password` fields are valid.

    This function does not do any sanity check over the fields given so please
    provide valid fields otherwise bot will end up submitting invalid fields
    resulting you to wait forever over the command line.

    Args:
      username: Username.
      password: User password.
    """
    if username is None:
      raise ValueError("Username field can't be empty.")
    if password is None:
      raise ValueError("Password field can't be empty.")

    driver.GetGlobalChromeDriverInstance().get(
        settings.GetLinkedInLoginPageUrl())

    username_elem = driver.GetGlobalChromeDriverInstance().find_element_by_name(
        LoginPageElements.get_username_element_name())
    username_elem.clear()
    username_elem.send_keys(username)

    password_elem = driver.GetGlobalChromeDriverInstance().find_element_by_name(
        LoginPageElements.get_password_element_name())
    password_elem.clear()
    password_elem.send_keys(password)

    password_elem.send_keys(keys.Keys.RETURN)

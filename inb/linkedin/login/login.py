"""
This module provides routines to communicate with the LinkedIn login page.

Before using this module be sure that the elements' path selectors inside the
class `_ElementsPathSelectors` are up to date.

```python
# Login to LinkedIn
from linkedin import login

login.LinkedIn.login('mohika@gmail.com', 'secretpassword')
```

Note: This module does not inform you about the invalidness of the credentials
in case the user name and password fields are incorrect.  So if the user is
using the bot in headless mode there's no way to tell the user that the fields
were incorrect and you need to restart the bot with valid fields.

@TODO(joshiayush): Show user that the given fields were invalid.

  :author: Ayush Joshi, ayush854032@gmail.com
  :copyright: Copyright (c) 2019 Creative Commons
  :license: BSD 3-Clause License, see license for details
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

import sys
import logging
import traceback

from selenium.common.exceptions import NoSuchElementException

from linkedin import (driver, settings)

from selenium.webdriver.common import keys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='w')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)


class _ElementsPathSelectors:
  """Stores path fields of the form elements."""

  @staticmethod
  def get_username_element_id() -> str:
    """Value for the name attribute of the `username` input element.

    Returns:
      Value for the name attribute of the `username` input element.
    """
    return 'username'

  @staticmethod
  def get_password_element_id() -> str:
    """Value for the name attribute of the `password` input element.

    Returns:
      Value for the name attribute of the `password` input element.
    """
    return 'password'


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

    Raises:
      ValueError: If the `username` or `password` is `None`.
    """
    if username is None:
      raise ValueError("Username field can't be empty.")
    if password is None:
      raise ValueError("Password field can't be empty.")

    driver.GetGlobalChromeDriverInstance().get(
        settings.GetLinkedInLoginPageUrl())

    try:
      username_elem = driver.GetGlobalChromeDriverInstance().find_element_by_id(
          _ElementsPathSelectors.get_username_element_id())
    except NoSuchElementException as exc:
      logger.critical(traceback.format_exc())
      raise exc
    else:
      username_elem.clear()
      username_elem.send_keys(username)

    try:
      password_elem = driver.GetGlobalChromeDriverInstance().find_element_by_id(
          _ElementsPathSelectors.get_password_element_id())
    except NoSuchElementException as exc:
      logger.critical(traceback.format_exc())
      raise exc
    else:
      password_elem.clear()
      password_elem.send_keys(password)

    password_elem.send_keys(keys.Keys.RETURN)

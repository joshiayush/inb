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

"""Utility module for the LinkedIn connect API."""

import sys
import logging
import traceback

from selenium.common import exceptions
from selenium.webdriver.common import by
from selenium.webdriver.remote import webelement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from linkedin import (driver, settings)
from linkedin.document_object_module import javascript
from linkedin.connect import pathselectorbuilder

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='a')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)


def GetElementByXPath(xpath: pathselectorbuilder.PathSelectorBuilder,
                      wait: int = 10) -> webelement.WebElement:
  """Returns an element from the `document_object_module` whose `xpath` is
  known.

  Function tries to find out an element from the `document_object_module` at
  the given `xpath` using the `WebDriverWait` API.  This function loads the page
  further immediately after the `WebDriverWait` API has raised
  `TimeoutException` in an hope that the element could be at the bottom of the
  page.

  THE MAIN CAVEAT here is that this function should only be used when you are
  completely sure that the element is going to reveal itself once you have
  scrolled the page a bit otherwise this function is going to stuck in an
  infinite loop and can only be stopped by the `KeyboardInterrupt` exception
  triggered explicitly.

  ```python
  # Taking the name out from the `document_object_module` using an explicit wait
  # routine.
  name = _GetElementByXPath(
      _MyNetworkPageElementsPathSelectors.get_suggestion_box_li_card_name_xpath(
          position)).text
  ```

  Args:
    xpath:  Element `xpath`.
    wait:   Time we should wait for until the element has popped itself to the
              `document_object_module`.

  Returns:
    `WebElement` located at the given `xpath`.
  """
  while True:
    try:
      return WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
          EC.presence_of_element_located((by.By.XPATH, str(xpath))))
    except exceptions.TimeoutException as exc:
      logger.critical('%s Element could not be found at: %s for label: %s',
                      traceback.format_exc().strip('\n').strip(), str(xpath),
                      xpath.path_label)
      if isinstance(exc, exceptions.TimeoutException):
        javascript.JS.load_page()
        continue

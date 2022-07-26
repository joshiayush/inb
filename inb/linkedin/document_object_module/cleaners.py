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
import logging
import traceback

from linkedin import (driver, settings)

from selenium.common import exceptions
from selenium.webdriver.common import by
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='a')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)

_FUNC_GET_ELEMENT_BY_XPATH_STR = """
function getElementByXpath(path) {
  return document.evaluate(path, document, null, 
    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}
"""


class _CleanerElementsSelectors:

  @staticmethod
  def get_message_overlay_css_selector() -> str:
    return "div[class^='msg-overlay-list-bubble']"

  @staticmethod
  def get_message_overlay_xpath() -> str:
    return "//*[@id='msg-overlay']"


class Cleaner:  # pylint: disable=missing-class-docstring

  @staticmethod
  def clear_message_overlay(wait: int = 60) -> None:
    try:
      WebDriverWait(driver.GetGlobalChromeDriverInstance(), wait).until(
          EC.presence_of_element_located(
              (by.By.CSS_SELECTOR,
               _CleanerElementsSelectors.get_message_overlay_css_selector())))
      driver.GetGlobalChromeDriverInstance().execute_script(f"""
        {_FUNC_GET_ELEMENT_BY_XPATH_STR}
        getElementByXpath(`{_CleanerElementsSelectors.get_message_overlay_xpath()}`).style = "display: none;";
      """)
    except (exceptions.NoSuchElementException, exceptions.TimeoutException):
      logger.critical(traceback.format_exc())

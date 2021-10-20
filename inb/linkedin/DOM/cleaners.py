# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!
from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.common.by import (
  By,
)
from selenium.webdriver.support import (
  expected_conditions as EC,
)
from selenium.webdriver.support.ui import (
  WebDriverWait,
)
from selenium.common.exceptions import (
  TimeoutException,
  NoSuchElementException,
)


class Cleaner(object):
  WAIT = 60
  MSG_OVERLAY_XPATH = "//*[@id='msg-overlay']"

  def __init__(self: Cleaner, driver: webdriver.Chrome) -> None:
    """Constructor method to initialize a Cleaner object.

    Args:
      self: (Cleaner) Self.
      driver: (webdriver.Chrome) Chromedriver.

    Raises:
      Exception: If 'driver' not given.

    Example:
    >>> from DOM import Cleaner
    >>> from selenium import webdriver
    >>>
    >>> chrome = webdriver.Chrome('your/chromedriver/path')
    >>> cleaner = Cleaner(chrome)
    """
    if not driver:
      raise Exception('webdriver.Chrome instance is not given!')
    self._driver = driver

  def clear_message_overlay(self: Cleaner, wait: int = None) -> None:
    """Method `clear_message_overlay()` clears the message overlay that overlaps the
    page. This is important as while sending invitation `selenium` will throw `exception`
    incase any element is overlapping the `invite` buttons.

    Args:
      self: (Cleaner) Self.
      wait: (int) Timeout.

    Example:
    >>> from DOM import Cleaner
    >>> from selenium import webdriver
    >>>
    >>> chrome = webdriver.Chrome('your/chromedriver/path')
    >>> cleaner = Cleaner(chrome)
    >>> cleaner.clear_message_overlay() # this will clear the message overlay lying of the screen
    """
    if not wait:
      wait = Cleaner.WAIT
    try:
      WebDriverWait(
          self._driver, wait).until(
          EC.presence_of_element_located(
              (By.CSS_SELECTOR,
               "div[class^='msg-overlay-list-bubble']")))
      self._driver.execute_script("""
                function getElementByXpath(path) {
                  return document.evaluate(
                      path, 
                      document, 
                      null, 
                      XPathResult.FIRST_ORDERED_NODE_TYPE, 
                      null
                    ).singleNodeValue;
                }
                getElementByXpath('%(msg_overlay_xpath)s').style = "display: none;";
                """ % {'msg_overlay_xpath': Cleaner.MSG_OVERLAY_XPATH})
    except (NoSuchElementException, TimeoutException):
      return

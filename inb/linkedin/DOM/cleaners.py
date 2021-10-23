"""
This module provides APIs to clean elements from document by setting their `display`
property to `none` while sending invitation and re-setting their `display` property to
normal before deleting the current instance.

  :author: Ayush Joshi, ayush854032@gmail.com
  :copyright: Copyright (c) 2019 Creative Commons.
  :license: MIT License, see license for details.
"""

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
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from urllib3.exceptions import MaxRetryError

from selenium.common.exceptions import (
  TimeoutException,
  NoSuchElementException,
)

FUNC_GET_ELEMENT_BY_XPATH = """
function getElementByXpath(path) {
  return document.evaluate(
    path, 
    document, 
    null, 
    XPathResult.FIRST_ORDERED_NODE_TYPE, 
    null
  ).singleNodeValue;
}
"""


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

    Variable `elements_marked_none` holds the elements the current instance
    marked as `display: none;`; this way before the instance dies we re-sets
    the 'display' property of those elements so if in case any process requires
    those elements in future it will not throw any kind of `NoSuchElementException`
    exception.

    Prototype:
    >>> [
    ...  {
    ...    element: webdriver.Chrome,
    ...    selector: str,
    ...    method: 'css|xpath|...',
    ...    original_display_value: str
    ...  }
    ... ]
    """
    if not driver:
      raise Exception('webdriver.Chrome instance is not given!')
    self._driver = driver
    self.elements_marked_none = []

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
      element = WebDriverWait(
          self._driver, wait).until(
          EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             "div[class^='msg-overlay-list-bubble']")
          )
      )
      selector = Cleaner.MSG_OVERLAY_XPATH
      method = 'xpath'
      original_display_value = element.value_of_css_property(
          'display')
      self._driver.execute_script(f"""
        {FUNC_GET_ELEMENT_BY_XPATH}
        getElementByXpath(`{Cleaner.MSG_OVERLAY_XPATH}`).style = "display: none;";
      """)
    except (NoSuchElementException, TimeoutException):
      return

    self.elements_marked_none.append(
      {'element': element, 'selector': selector, 'method': method,
       'original_display_value': original_display_value})

  def __del__(self: Cleaner) -> None:
    """Destructor re-sets elements original state before deleting current instance.

    This is neccessary as if in case any other process wants to access the element
    that we removed earlier, selenium will throw `NoSuchElementException` as it won't
    be able to locate that element as we've already removed it from the document.

    This destructor method takes care of the above issue from happening by re-setting
    every elements' state back to normal.

    Args:
      self: (Cleaner) Self.

    Example:
    >>> from DOM import Cleaner
    >>> from selenium import webdriver
    >>>
    >>> chrome = webdriver.Chrome('your/chromedriver/path')
    >>> cleaner = Cleaner(chrome)
    >>>
    >>> # this will clear the message overlay lying of the screen by setting display to none
    >>> cleaner.clear_message_overlay() 
    >>> # this will set the message overlay item to its original state
    >>> del cleaner
    """
    try:
      for element in self.elements_marked_none:
        if element['method'] == 'xpath':
          self._driver.execute_script(f"""
            {FUNC_GET_ELEMENT_BY_XPATH}
            getElementByXpath(`{element['selector']}`).style = "display: {element['original_display_value']};";
          """)
        elif element['method'] == 'css':
          self._driver.execute_script(f"""
            document.querySelector(`{element['selector']}`).style = "display: {element['original_display_value']}"
            """)
    except MaxRetryError:
      pass

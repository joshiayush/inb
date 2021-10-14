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

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


class Cleaner(object):
  WAIT: int = 60
  MSG_OVERLAY_XPATH: str = "//*[@id='msg-overlay']"

  def __init__(self: Cleaner, driver: webdriver.Chrome) -> None:
    """Constructor method to initialize a Cleaner object.

    :Args:
        - self: {Cleaner} self.
        - driver: {webdriver} Chromedriver

    :Raises:
        - {Exception} if 'driver' object is not a 'webdriver' instance.
    """
    if not isinstance(driver, webdriver.Chrome):
      raise Exception(
          "'%(driver_type)s' object is not a 'webdriver' object" %
          {"driver_type": type(driver)})
    self._driver = driver

  def clear_message_overlay(self: Cleaner, wait: int = 60) -> None:
    """Function clear_msg_overlay() clears the message overlay that gets on the top of the
    network page.

    :Args:
        - self: {Cleaner} object from which 'driver' property has to accessed.
        - wait: {int} timeout

    :Returns:
        - {None}
    """
    if not isinstance(wait, int):
      wait = Cleaner.WAIT

    try:
      WebDriverWait(
          self._driver, wait).until(
          EC.presence_of_element_located(
              (By.CSS_SELECTOR,
               "div[class^='msg-overlay-list-bubble']")))
      self._driver.execute_script(
          """
                function getElementByXpath(path) {
                  return document.evaluate(
                      path, 
                      document, 
                      null, 
                      XPathResult.FIRST_ORDERED_NODE_TYPE, 
                      null
                    ).singleNodeValue;
                }
                getElementByXpath("%(msg_overlay_xpath)s").style = "display: none;";
                """ % {"msg_overlay_xpath": Cleaner.MSG_OVERLAY_XPATH})
    except (NoSuchElementException, TimeoutException):
      return

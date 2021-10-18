"""
This module provides a `Driver` class to instantiate a chromedriver object 
for our `inb` program. 

This currently only supports `chromedriver` but there are future plans to add
support for `Tor` browser to stay annonymous while scraping through tons of
webpages just to gather information about a certain `company` or `person`.

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

import json

from selenium import webdriver

from errors import WebDriverPathNotGivenException
from errors import WebDriverNotExecutableException

from lib.utils.validator import Validator

__version__: str = "3.109.59"


class Driver(object):
  # minimum chromedriver options required for our purpose
  OPTIONS = {
    # allow execution of the full version of the latest chrome driver
    # without GPU
    'headless': '--headless',
    # enable safe mode to avoid leaving prints behind of any of the
    # classified data
    'incognito': '--incognito',
    # not recommended to use it, enabling this option may allow
    # attackers to impersonate you and steal your information using
    # an attack called Self-XSS -- do not use this option if you don't
    # know what you are doing; this is highly vulnerable not only your
    # information is at risk but the available sessions too
    'no-sandbox': '--no-sandbox',
    # allow execution of the full version of the latest chrome driver
    # without GPU (only requires for Windows OS)
    'disable-gpu': '--disable-gpu',
    # start chrome window in maximized mode even if running headless
    'start-maximized': '--start-maximized',
    # to disable the notification 'Chrome is being controlled by
    # automated test software'
    'disable-infobars': '--disable-infobars',
    # works similar to '--disable-infobars'; use this option with
    # higher versions of chromedriver
    'enable-automation': '--enable-automation',
    # disable currently installed chrome extensions to keep your
    # data safe while browsing
    'disable-extensions': '--disable-extensions',
    # disable notifications when running chromedriver for automation
    # testing
    'disable-notifications': '--disable-notifications',
    # disable SUID binary
    'disable-setuid-sandbox': '--disable-setuid-sandbox',
    # disable certificate errors for visiting non-https sites as https
    'ignore-certificate-errors': '--ignore-certificate-errors',
    # set this flag if running chromedriver in headless mode otherwise
    # many elements will fall beyond the current page view
    'default-headless-window-size': 'window-size=1200,1100'
  }

  def __init__(self: Driver, driver_path: str = None, options: list = []) -> None:
    """Constructor method constructs a `Driver` instance to communicate with
    chromedriver.

    Optionally it takes in chromedriver's command-line arguments to activate
    or deactivate chromedriver's features that are not required for the session. 

    Args:
      self: (Driver) Self.
      driver_path: (str) Chromedriver's path.
      options: (list) Chromedriver's command-line options.

    Raises:
      WebDriverNotExecutableException: In case the `driver_path` given is not a 
        valid path or the chromedriver's binary is not executable.
      WebDriverPathNotGivenException: In case `driver_path` is `None`.

    Example:
    >>> from linkedin import Driver
    >>> from lib import chromedriver_abs_path
    >>>
    >>> # Instantiate chromedriver without options
    >>> chromedriver = Driver(chromedriver_abs_path())
    >>> chromedriver.enable_webdriver_chrome()
    >>> print(chromedriver)

    <selenium.webdriver.chrome.webdriver.WebDriver (session="b15ea4e4ed12d09201bc2b3771918ff9") 
      (driver_path="/Python/inb/driver/chromedriver")>

    >>> # Instantiate chromedriver with options
    >>> chromedriver = Driver(chromedriver_abs_path(), [Driver.OPTIONS['headless'],
    >>>                 Driver.OPTIONS['incognito'], ...])
    >>> chromedriver.enable_webdriver_chrome()
    >>> print(chromedriver)

    <selenium.webdriver.chrome.webdriver.WebDriver (session="b15ea4e4ed12d09201bc2b3771918ff9") 
      (driver_path="/Python/inb/driver/chromedriver") (options="[--headless, --incognito, ...]")>
    """
    if driver_path:
      if not Validator(driver_path).is_executable():
        raise WebDriverNotExecutableException(
            '%(path)s is not executable!' % {'path': driver_path})
    else:
      raise WebDriverPathNotGivenException(
          "User did not provide chromedriver's path!\n" +
          "Currently 'Driver' class does not support instantiation without chromedriver's binary path!")
    self._driver_path = driver_path
    self._options = webdriver.ChromeOptions()

    if len(options) > 0:
      for arg in options:
        self._options.add_argument(arg)
    self.enable_webdriver_chrome()

  def __repr__(self: Driver) -> str:
    """Method `__repr__()` returns a formatted string containing the session,
    driver path and options' (if given) information of the current `Driver` instance.

    Args:
      self: (Driver) Self.

    Returns:
      Formatted string containing the session, driver path and options' (if given) 
        information of the current `Driver` instance.

    Example:
    >>> from linkedin import Driver
    >>> from lib import chromedriver_abs_path

    >>> chromedriver = Driver(chromedriver_abs_path())
    >>> chromedriver.enable_webdriver_chrome()
    >>> print(chromedriver)

    <selenium.webdriver.chrome.webdriver.WebDriver (session="b15ea4e4ed12d09201bc2b3771918ff9") 
      (driver_path="/Python/inb/driver/chromedriver")>
    """
    if len(self._options.arguments) == 0:
      return '<{0.__module__}.{0.__name__} (session="{1}") (driver_path="{2}")>'.format(
          type(self), self.driver.session_id, self._driver_path)
    else:
      return '<{0.__module__}.{0.__name__} (session="{1}") (driver_path="{2}") (options="{3}")>'.format(
          type(self), self.driver.session_id, self._driver_path, json.dumps(self._options.arguments, separators=(', ', ':')))

  def enable_webdriver_chrome(self: Driver) -> None:
    """Method `enable_web_driver()` creates a driver instance by calling the `Chrome`
    constructor.

    Args:
      self: (Driver) Self.

    Example:
    >>> from linkedin import Driver
    >>> from lib import chromedriver_abs_path

    >>> chromedriver = Driver(chromedriver_abs_path())
    >>> chromedriver.enable_webdriver_chrome()
    """
    self.driver = webdriver.Chrome(
        self._driver_path, options=self._options)

  def disable_webdriver_chrome(self: Driver) -> None:
    """Method `disable_webdriver_chrome()` closes the webdriver session by
    invoking the destructor on itself.

    Args:
      self: (Driver) Self.

    Example:
    >>> from linkedin import Driver
    >>> from lib import chromedriver_abs_path

    >>> chromedriver = Driver(chromedriver_abs_path())
    >>> chromedriver.enable_webdriver_chrome()
    >>> chromedriver.disable_webdriver_chrome()
    """
    del self

  def __del__(self: Driver) -> None:
    """Destructor method deletes the current `driver` instance.

    Args:
      self: (Driver) Self.

    Example:
    >>> from linkedin import Driver
    >>> from lib import chromedriver_abs_path

    >>> chromedriver = Driver(chromedriver_abs_path())
    >>> chromedriver.enable_webdriver_chrome()
    >>> # Delete 'chromedriver' instance
    >>> del chromedriver
    """
    self.driver.quit()

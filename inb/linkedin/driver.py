"""Instantiate and serves a single `webdriver.Chrome` instance all over the
running process.

```python
GChromeDriverInstance.initialize('/path/to/chromedriver', ['--headless', ...])

element = GetGlobalChromeDriverInstance().find_element_by_id('identifier')
DisableGlobalChromeDriverInstance()
```
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

from typing import List

import sys
import logging
import traceback

from selenium import webdriver
from selenium.common import exceptions

from linkedin import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='w')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)

CHROMEDRIVER_OPTIONS = {
    # start chrome window in maximized mode even if running headless
    'start-maximized': '--start-maximized',
    # not recommended to use it, enabling this option may allow attackers to
    # impersonate you and steal your information using an attack called
    # Self-XSS -- do not use this option if you don't know what you are doing;
    # this is highly vulnerable not only your information is at risk but the
    # available sessions too
    'no-sandbox': '--no-sandbox',
    'disable-dev-shm-usage': '--disable-dev-shm-usage',
    # set this flag if running chromedriver in headless mode otherwise many
    # elements will fall beyond the current page view
    'default-headless-window-size': 'window-size=1200,1100',
    # allow execution of the full version of the latest chrome driver without
    # GPU
    'headless': '--headless',
    # disable SUID binary
    'disable-setuid-sandbox': '--disable-setuid-sandbox',
    # disable certificate errors for visiting non-https sites as https
    'ignore-certificate-errors': '--ignore-certificate-errors',
    # works similar to '--disable-infobars'; use this option with higher
    # versions of chromedriver
    'enable-automation': '--enable-automation',
    # enable safe mode to avoid leaving prints behind of any of the classified
    # data
    'incognito': '--incognito',
    # allow execution of the full version of the latest chrome driver without
    # GPU (only requires for Windows OS)
    'disable-gpu': '--disable-gpu',
    # to disable the notification 'Chrome is being controlled by automated test
    # software.
    'disable-infobars': '--disable-infobars',
    # disable currently installed chrome extensions to keep your data safe while
    # browsing
    'disable-extensions': '--disable-extensions',
    # disable notifications when running chromedriver for automation testing
    'disable-notifications': '--disable-notifications',
    # @TODO(joshiayush): Add useful arguments here...
}


class _Driver(object):
  """Module specific implementation to instantiate and serve a single
  `webdriver.Chrome` instance in the running process.
  """

  def __init__(self) -> None:
    self.driver = None

  def enable_webdriver_chrome(
      self, chromedriver_path: str,
      chromedriver_options: List[str]) -> webdriver.Chrome:
    """Enables `webdriver.Chrome` instance using the `chromedriver` path and
    options.

    This method takes in `chromedriver_path` and `chromedriver_options` and
    instantiates a `webdriver.Chrome` object.  In case `chromedriver_path` is
    `None` this function will then look into the system's `binary` path for
    `chromedriver` executable.

    Note: This function does not do any kind of sanity check on
    `chromedriver_path`, in case you give an invalid executable path then you
    will get a `WebDriverException` thrown at you. Be careful with the path.

    Args:
      chromedriver_path: Chrome driver executable path.
      chromedriver_options: Chrome driver command line options.
    """
    if self.driver:
      return

    if not chromedriver_path:
      chromedriver_path = 'chromedriver'

    self.options = webdriver.ChromeOptions()
    if chromedriver_options:
      for chromedriver_option in chromedriver_options:
        self.options.add_argument(chromedriver_option)

    self.driver = webdriver.Chrome(chromedriver_path, options=self.options)

  def disable_webdriver_chrome(self) -> None:
    """Disables the `webdriver.Chrome` instance.

    This function disables the `webdriver.Chrome` instance by calling the
    `quit()` method on the `webdriver.Chrome` instance.
    """
    if not self.driver:
      return
    self.driver.quit()
    self.driver = None

  def __del__(self) -> None:
    """Disables the `webdriver.Chrome` instance.

    This function disables the `webdriver.Chrome` instance by calling
    `disable_webdriver_chrome()` method which internally calls the `quit()`
    method on the `webdriver.Chrome` instance.
    """
    self.disable_webdriver_chrome()


_DRIVER = _Driver()


class GChromeDriverInstance:
  """Global class to initialize global set of `chromedriver` path and options.
  """
  CHROMEDIRVER_PATH = None
  CHROMEDRIVER_OPTIONS = None

  @staticmethod
  def initialize(
      chromedriver_path: str = None,
      chromedriver_options: List[str] = None,
  ) -> None:
    """Initializes global set of `chromedriver` path and options.

    This function takes in `chromedriver_path` and `chromedriver_options` and
    initialzes class' static data member `CHROMEDIRVER_PATH` and
    `CHROMEDRIVER_OPTIONS` with the given values respectively.

    Args:
      chromedriver_path: Chrome driver executable path.
      chromedriver_options: Chrome driver's command line options.
    """
    GChromeDriverInstance.CHROMEDIRVER_PATH = chromedriver_path
    GChromeDriverInstance.CHROMEDRIVER_OPTIONS = chromedriver_options


def GetGlobalChromeDriverInstance(
    exception: Exception = exceptions.WebDriverException) -> webdriver.Chrome:
  """Returns a `chromedriver` instance located at the path
  `GChromeDriverInstance.CHROMEDIRVER_PATH`.

  This function uses `GChromeDriverInstance.CHROMEDIRVER_PATH` as the
  `chromedriver` executable path and returns `webdriver.Chrome` instance.
  This function does not do any sanity check for the initialized
  `GChromeDriverInstance.CHROMEDIRVER_PATH`.

  In case the `GChromeDriverInstance.CHROMEDIRVER_PATH` given is `None` then
  this function tries to search for the `chromedriver` executable in the
  system's `binary` path.

  If `GChromeDriverInstance.CHROMEDRIVER_OPTIONS` is not `None` then this
  function will also enable the `chromedriver` options present in the
  `chromedriver_options` list.

  Note: Before executing this function make sure that the `chromedriver` exists
  in `GChromeDriverInstance.CHROMEDIRVER_PATH` and is executable otherwise this
  function will raise `WebDriverException`.

  In addition to enabling `webdriver.Chrome` instance this function also logs
  the stacktrace of the `WebDriverException` inside the `logs` directory for
  later debugging.

  ```python
  import traceback

  try:
    chromedriver = GetWebDriverChromeFromChromeDriverExecPath(
                    exception=exceptions.WebDriverException)
  except exceptions.WebDriverException as exc:
    logger.error(traceback.format_exc())
    raise exc
  ```

  You may also notice that this function takes in an argument called `exception`
  which is used to decide which exception to raise in case of a failure.  This
  logic comes in handy while debugging and while used in production.  While
  using inb in production we give this function an exception that our `cli` is
  familiar with to print a nice little message to the user to describe where the
  problem is rather than printing a complete stack trace.

  ```python
  import traceback

  try:
    chromedriver = GetWebDriverChromeFromChromeDriverExecPath(
                      exception=CliFamiliarException)
  except exceptions.WebDriverException as exc:
    logger.error(traceback.format_exc())
    raise exc
  ```

  Note: When called multiple times this function is not going to return
  different `chromedriver` instances, you will receive the same object that
  you received the first time you called this function no matter how many
  times you call this function again.

  Args:
    exception: Exception to raise in case of failure.

  Returns:
    `webdriver.Chrome` instance.

  Raises:
    Raises exception given in function argument i.e., `exception`.
  """
  try:
    _DRIVER.enable_webdriver_chrome(GChromeDriverInstance.CHROMEDIRVER_PATH,
                                    GChromeDriverInstance.CHROMEDRIVER_OPTIONS)
  except exceptions.WebDriverException as exc:
    logger.critical(traceback.format_exc())
    if isinstance(exc, exception):
      raise exc
    raise exception(str(exc)) from exc
  else:
    return _DRIVER.driver


def DisableGlobalChromeDriverInstance() -> None:
  """Disables the `webdriver.Chrome` instance inside of `_DRIVER` instance.

  This function disables the `webdriver.Chrome` instance inside of `_DRIVER`
  instance by calling `disable_webdriver_chrome()` method which internally calls
  the `quit()` method on the `webdriver.Chrome` instance.

  Note: After calling this method you will be able to create a new
  `webdriver.Chrome` instance with new `chromedriver` path and options.
  """
  _DRIVER.disable_webdriver_chrome()

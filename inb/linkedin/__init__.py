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

from errors import WebDriverPathNotGivenException
from errors import WebDriverNotExecutableException

from lib.utils.validator import Validator

__version__: str = "1.51.35"


class Driver(object):
    __SESSION_ALREADY_EXISTS: bool = False

    HEADLESS: str = "--headless"
    INCOGNITO: str = "--incognito"
    NO_SANDBOX: str = "--no-sandbox"
    DISABLE_GPU: str = "--disable-gpu"
    START_MAXIMIZED: str = "--start-maximized"
    DISABLE_INFOBARS: str = "--disable-infobars"
    ENABLE_AUTOMATION: str = "--enable-automation"
    DISABLE_EXTENSIONS: str = "--disable-extensions"
    DISABLE_NOTIFICATIONS: str = "--disable-notifications"
    DISABLE_SETUID_SANDBOX: str = "--disable-setuid-sandbox"
    IGNORE_CERTIFICATE_ERRORS: str = "--ignore-certificate-errors"

    def __init__(self: Driver, driver_path: str, options: list = []) -> None:
        if isinstance(driver_path, str):
            if driver_path.strip() == '':
                raise WebDriverPathNotGivenException(
                    "User did not provide chromedriver's path!")
            if not Validator(driver_path).is_executable():
                raise WebDriverNotExecutableException(
                    "%(path)s is not executable!" % {"path": driver_path})
        else:
            raise WebDriverPathNotGivenException(
                "User did not provide chromedriver's path!")

        self._driver_path = driver_path
        self._options = webdriver.ChromeOptions()

        if not len(options) == 0:
            for arg in options:
                self._options.add_argument(arg)

        self.enable_webdriver_chrome()

    def enable_webdriver_chrome(self: Driver) -> None:
        """Method enable_web_driver() makes a webdriver object called by calling 
        'webdriver.Chrome()' constructor.

        :Args:
            - self: {LinkedIn} object
            - _options: {Options} to pass to webdriver.Chrome() constructor

        :Returns:
            - {None}

        """
        if Driver.__SESSION_ALREADY_EXISTS:
            return

        Driver.__SESSION_ALREADY_EXISTS = True

        self.driver = webdriver.Chrome(self._driver_path,
                                       options=self._options)

    def disable_webdriver_chrome(self: Driver) -> None:
        """Method disable_webdriver_chrome() closes the webdriver session by 
        executing a function called 'close()' on webdriver object.

        :Args:
            - self: {LinkedIn} object

        :Returns:
            - {None}
        """
        Driver.__SESSION_ALREADY_EXISTS = False
        self.driver.quit()

    def __del__(self: Driver) -> None:
        Driver.__SESSION_ALREADY_EXISTS = False
        self.driver.quit()

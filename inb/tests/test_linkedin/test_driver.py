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

import os
import stat
import unittest

from unittest.mock import call
from unittest.mock import Mock
from unittest.mock import patch

from linkedin import Driver

from lib import DRIVER_PATH
from errors import WebDriverPathNotGivenException
from errors import WebDriverNotExecutableException


class TestDriverClass(unittest.TestCase):

    @unittest.skipIf(not os.getuid() == 0, "Requires root privileges!")
    def test_constructor_method_with_invalid_executable_path(self: TestDriverClass) -> None:
        paths = [1, (1, 2, 3), [1, 2, 3], {1: 1, 2: 2}]
        for path in paths:
            with self.assertRaises(WebDriverPathNotGivenException):
                driver = Driver(path)

        original_file_permissions = stat.S_IMODE(os.lstat(DRIVER_PATH).st_mode)

        def remove_execute_permissions(path):
            """Remove write permissions from this path, while keeping all other 
            permissions intact.

            Params:
                path:  The path whose permissions to alter.
            """
            NO_USER_EXECUTE = ~stat.S_IXUSR
            NO_GROUP_EXECUTE = ~stat.S_IXGRP
            NO_OTHER_EXECUTE = ~stat.S_IXOTH
            NO_EXECUTE = NO_USER_EXECUTE & NO_GROUP_EXECUTE & NO_OTHER_EXECUTE

            current_permissions = stat.S_IMODE(os.lstat(path).st_mode)
            os.chmod(path, current_permissions & NO_EXECUTE)

        remove_execute_permissions(DRIVER_PATH)
        with self.assertRaises(WebDriverNotExecutableException):
            driver = Driver(driver_path=DRIVER_PATH)

        # place the original file permissions back
        os.chmod(DRIVER_PATH, original_file_permissions)

    @patch("linkedin.Driver.enable_webdriver_chrome")
    def test_constructor_method_with_valid_chromedriver_path(self: TestDriverClass, mock_enable_webdriver_chrome: Mock) -> None:
        driver = Driver(driver_path=DRIVER_PATH)
        mock_enable_webdriver_chrome.assert_called()

    @patch("selenium.webdriver.ChromeOptions.add_argument")
    def test_constructor_method_add_argument_internal_calls(self: TestDriverClass, mock_add_argument: Mock) -> None:
        calls = [call(Driver.HEADLESS), call(Driver.INCOGNITO), call(Driver.NO_SANDBOX), call(Driver.DISABLE_GPU),
                 call(Driver.START_MAXIMIZED), call(
                     Driver.DISABLE_INFOBARS), call(Driver.ENABLE_AUTOMATION),
                 call(Driver.DISABLE_EXTENSIONS), call(
                     Driver.DISABLE_NOTIFICATIONS), call(Driver.DISABLE_SETUID_SANDBOX),
                 call(Driver.IGNORE_CERTIFICATE_ERRORS)]
        driver = Driver(driver_path=DRIVER_PATH, options=[
                        Driver.HEADLESS, Driver.INCOGNITO, Driver.NO_SANDBOX, Driver.DISABLE_GPU, Driver.START_MAXIMIZED,
                        Driver.DISABLE_INFOBARS, Driver.ENABLE_AUTOMATION, Driver.DISABLE_EXTENSIONS, Driver.DISABLE_NOTIFICATIONS,
                        Driver.DISABLE_SETUID_SANDBOX, Driver.IGNORE_CERTIFICATE_ERRORS])
        mock_add_argument.assert_has_calls(calls)

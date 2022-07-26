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

import os
import unittest

from unittest import mock
from selenium import webdriver
from selenium.common import exceptions

import lib
from linkedin import (driver, settings)


def _GetAddArgumentCallingOrder() -> list[str]:
  return [
      driver.CHROMEDRIVER_OPTIONS['no-sandbox'],
      driver.CHROMEDRIVER_OPTIONS['disable-dev-shm-usage'],
      driver.CHROMEDRIVER_OPTIONS['start-maximized'],
      driver.CHROMEDRIVER_OPTIONS['incognito'],
      driver.CHROMEDRIVER_OPTIONS['enable-automation'],
      driver.CHROMEDRIVER_OPTIONS['disable-setuid-sandbox'],
      driver.CHROMEDRIVER_OPTIONS['disable-gpu'],
      driver.CHROMEDRIVER_OPTIONS['headless'],
      driver.CHROMEDRIVER_OPTIONS['disable-notifications'],
      driver.CHROMEDRIVER_OPTIONS['disable-infobars'],
      driver.CHROMEDRIVER_OPTIONS['ignore-certificate-errors'],
      driver.CHROMEDRIVER_OPTIONS['disable-extensions'],
  ]


class TestProtectedDriverClass(unittest.TestCase):  # pylint: disable=missing-class-docstring

  def setUp(self) -> None:
    self.driver = driver._Driver()  # pylint: disable=protected-access

  @lib.IgnoreWarnings(ResourceWarning)
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_only_path(
      self, mk_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(settings.ChromeDriverAbsolutePath(),
                                          None)
      mk_add_argument.assert_not_called()
    except exceptions.WebDriverException as exc:
      self.fail('enable_webdriver_chrome(%(path)s, None) failed with %(msg)s.' %
                {
                    'path': settings.ChromeDriverAbsolutePath(),
                    'msg': str(exc)
                })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received ' # pylint: disable=consider-using-f-string
           '%(type)s') % {'type': lib.Type(self.driver.driver)})

  @lib.IgnoreWarnings(ResourceWarning)
  @unittest.skipIf(
      not lib.Which('chromedriver'),
      ('Chromedriver executable is not present in the environment PATH.\n'
       'Check if the x bit is OK in case environment PATH exists.'))
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_set_to_none(
      self, mk_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(None, None)
      mk_add_argument.assert_not_called()
    except exceptions.WebDriverException as exc:
      self.fail('enable_webdriver_chrome(%(path)s, None) failed with %(msg)s.' %
                {
                    'path': settings.ChromeDriverAbsolutePath(),
                    'msg': str(exc)
                })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '  # pylint: disable=consider-using-f-string
           '%(type)s') % {'type': lib.Type(self.driver.driver)})

  @lib.IgnoreWarnings(ResourceWarning)
  @unittest.skipIf(
      not lib.Which('chromedriver'),
      ('Chromedriver executable is not present in the environment PATH.\n'
       'Check if the x bit is OK in case environment PATH exists.'))
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_set_to_none_but_options_given(
      self, mk_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(settings.ChromeDriverAbsolutePath(),
                                          _GetAddArgumentCallingOrder())
      mk_add_argument.assert_has_calls(
          [mock.call(option) for option in _GetAddArgumentCallingOrder()])
    except exceptions.WebDriverException as exc:
      self.fail(
          'enable_webdriver_chrome(%(path)s, %(opts)s) failed with %(msg)s.' % {
              'path': settings.ChromeDriverAbsolutePath(),
              'opts': _GetAddArgumentCallingOrder(),
              'msg': str(exc)
          })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '  # pylint: disable=consider-using-f-string
           '%(type)s') % {'type': lib.Type(self.driver.driver)})

  @lib.IgnoreWarnings(ResourceWarning)
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_and_options(
      self, mk_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(settings.ChromeDriverAbsolutePath(),
                                          _GetAddArgumentCallingOrder())
      mk_add_argument.assert_has_calls(
          [mock.call(option) for option in _GetAddArgumentCallingOrder()])
    except exceptions.WebDriverException as exc:
      self.fail(
          'enable_webdriver_chrome(%(path)s, %(opts)s) failed with %(msg)s.' % {
              'path': settings.ChromeDriverAbsolutePath(),
              'opts': _GetAddArgumentCallingOrder(),
              'msg': str(exc)
          })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '  # pylint: disable=consider-using-f-string
           '%(type)s') % {'type': lib.Type(self.driver.driver)})

  def tearDown(self) -> None:
    del self.driver


class TestProtectedMemberDriver(unittest.TestCase):

  def test_if_protected_member_driver_is_instance_of_driver(self) -> None:
    self.assertIsInstance(driver._DRIVER, driver._Driver)  # pylint: disable=protected-access


class TestGChromeDriverInstanceClass(unittest.TestCase):

  def test_if_initialize_method_sets_static_method(self) -> None:
    driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsolutePath(),
                                            _GetAddArgumentCallingOrder())
    self.assertEqual(driver.GChromeDriverInstance.CHROMEDIRVER_PATH,
                     settings.ChromeDriverAbsolutePath())
    self.assertEqual(driver.GChromeDriverInstance.CHROMEDRIVER_OPTIONS,
                     _GetAddArgumentCallingOrder())


class TestGetGlobalChromeDriverInstanceMethod(unittest.TestCase):  # pylint: disable=missing-class-docstring

  def setUp(self) -> None:
    driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsolutePath(),
                                            _GetAddArgumentCallingOrder())

  @lib.IgnoreWarnings(ResourceWarning)
  def test_with_no_arguments(self) -> None:
    self.assertIsInstance(driver.GetGlobalChromeDriverInstance(),
                          webdriver.Chrome)

  @lib.IgnoreWarnings(ResourceWarning)
  @mock.patch('logging.Logger.critical')
  def test_with_invalid_fields(self, mk_logger_critical: mock.Mock) -> None:
    driver.GChromeDriverInstance.initialize(
        settings.ChromeDriverAbsolutePath()
        [:settings.ChromeDriverAbsolutePath().find('chromedriver')],
        _GetAddArgumentCallingOrder())

    with self.assertRaises(exceptions.WebDriverException):
      _ = driver.GetGlobalChromeDriverInstance()

    mk_logger_critical.assert_called()

  @lib.IgnoreWarnings(ResourceWarning)
  @unittest.skipIf(
      not os.getuid() == 0,
      ('\nThis test case requires to be ran as root!\n'
       'You need to run this test suite separately using,\n'
       'python3 inb/test.py TestRemoveFilePermissionsFunction.test_name\n'))
  def test_when_x_bit_is_off(self) -> None:
    """Note: This test case should be ran over command line as root using,

    ```shell
    python3 inb/test.py TestGetGlobalChromeDriverInstanceMethod
      .test_when_x_bit_is_off
    ```
    """
    lib.RemoveFilePermissions(settings.ChromeDriverAbsolutePath(), 'x')

    with self.assertRaises(exceptions.WebDriverException):
      _ = driver.GetGlobalChromeDriverInstance()

    lib.AddFilePermissions(settings.ChromeDriverAbsolutePath(), 'x')

  def tearDown(self) -> None:
    driver.DisableGlobalChromeDriverInstance()


class TestDisableGlobalChromeDriverInstanceMethod(unittest.TestCase):  # pylint: disable=missing-class-docstring

  @lib.IgnoreWarnings(ResourceWarning)
  @mock.patch('selenium.webdriver.Chrome.quit')
  def test_disable_global_chromedriver_instance_method(
      self, mk_quit: mock.Mock) -> None:
    driver.GChromeDriverInstance.initialize(settings.ChromeDriverAbsolutePath(),
                                            _GetAddArgumentCallingOrder())
    driver_ = driver.GetGlobalChromeDriverInstance()
    self.assertIsInstance(driver_, webdriver.Chrome)
    self.assertEqual(driver_, driver._DRIVER.driver)  # pylint: disable=protected-access
    driver.DisableGlobalChromeDriverInstance()
    mk_quit.assert_called()
    self.assertIsNone(driver._DRIVER.driver)  # pylint: disable=protected-access

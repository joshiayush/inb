# pylint: disable=missing-module-docstring

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

from __future__ import annotations

import os
from typing import List

import unittest

from unittest import mock
from selenium import webdriver
from selenium.common import exceptions

from lib import utils
from linkedin import (driver, settings)


def _GetAddArgumentCallingOrder() -> List[str]:
  return [
      driver.CHROMEDRIVER_OPTIONS['start-maximized'],
      driver.CHROMEDRIVER_OPTIONS['incognito'],
      driver.CHROMEDRIVER_OPTIONS['enable-automation'],
      driver.CHROMEDRIVER_OPTIONS['no-sandbox'],
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

  @utils.IgnoreWarnings(ResourceWarning)
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_only_path(
      self, mock_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(settings.CHROME_DRIVER_ABS_PATH, None)
      mock_add_argument.assert_not_called()
    except exceptions.WebDriverException as exc:
      self.fail('enable_webdriver_chrome(%(path)s, None) failed with %(msg)s.' %
                {
                    'path': settings.CHROME_DRIVER_ABS_PATH,
                    'msg': str(exc)
                })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '
           '%(type)s') % {'type': utils.Type(self.driver.driver)})

  @utils.IgnoreWarnings(ResourceWarning)
  @unittest.skipIf(
      not utils.Which('chromedriver'),
      ('Chromedriver executable is not present in the environment PATH.\n'
       'Check if the x bit is OK in case environment PATH exists.'))
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_set_to_none(
      self, mock_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(None, None)
      mock_add_argument.assert_not_called()
    except exceptions.WebDriverException as exc:
      self.fail('enable_webdriver_chrome(%(path)s, None) failed with %(msg)s.' %
                {
                    'path': settings.CHROME_DRIVER_ABS_PATH,
                    'msg': str(exc)
                })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '
           '%(type)s') % {'type': utils.Type(self.driver.driver)})

  @utils.IgnoreWarnings(ResourceWarning)
  @unittest.skipIf(
      not utils.Which('chromedriver'),
      ('Chromedriver executable is not present in the environment PATH.\n'
       'Check if the x bit is OK in case environment PATH exists.'))
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_set_to_none_but_options_given(
      self, mock_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(settings.CHROME_DRIVER_ABS_PATH,
                                          _GetAddArgumentCallingOrder())
      mock_add_argument.assert_has_calls(
          [mock.call(option) for option in _GetAddArgumentCallingOrder()])
    except exceptions.WebDriverException as exc:
      self.fail(
          'enable_webdriver_chrome(%(path)s, %(opts)s) failed with %(msg)s.' % {
              'path': settings.CHROME_DRIVER_ABS_PATH,
              'opts': _GetAddArgumentCallingOrder(),
              'msg': str(exc)
          })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '
           '%(type)s') % {'type': utils.Type(self.driver.driver)})

  @utils.IgnoreWarnings(ResourceWarning)
  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_and_options(
      self, mock_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(settings.CHROME_DRIVER_ABS_PATH,
                                          _GetAddArgumentCallingOrder())
      mock_add_argument.assert_has_calls(
          [mock.call(option) for option in _GetAddArgumentCallingOrder()])
    except exceptions.WebDriverException as exc:
      self.fail(
          'enable_webdriver_chrome(%(path)s, %(opts)s) failed with %(msg)s.' % {
              'path': settings.CHROME_DRIVER_ABS_PATH,
              'opts': _GetAddArgumentCallingOrder(),
              'msg': str(exc)
          })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '
           '%(type)s') % {'type': utils.Type(self.driver.driver)})

  def tearDown(self) -> None:
    del self.driver


class TestProtectedMemberDriver(unittest.TestCase):

  def test_if_protected_member_driver_is_instance_of_driver(self) -> None:
    self.assertIsInstance(driver._DRIVER, driver._Driver)  # pylint: disable=protected-access


class TestGChromeDriverInstanceClass(unittest.TestCase):

  def test_if_initialize_method_sets_static_method(self) -> None:
    driver.GChromeDriverInstance.initialize(settings.CHROME_DRIVER_ABS_PATH,
                                            _GetAddArgumentCallingOrder())
    self.assertEqual(driver.GChromeDriverInstance.CHROMEDIRVER_PATH,
                     settings.CHROME_DRIVER_ABS_PATH)
    self.assertEqual(driver.GChromeDriverInstance.CHROMEDRIVER_OPTIONS,
                     _GetAddArgumentCallingOrder())


class TestGetGlobalChromeDriverInstanceMethod(unittest.TestCase):

  def setUp(self) -> None:
    driver.GChromeDriverInstance.initialize(settings.CHROME_DRIVER_ABS_PATH,
                                            _GetAddArgumentCallingOrder())

  def test_get_global_chrome_driver_instance_method_with_no_arguments(
      self) -> None:
    self.assertIsInstance(driver.GetGlobalChromeDriverInstance(),
                          webdriver.Chrome)

  @mock.patch('logging.Logger.critical')
  def test_get_global_chrome_driver_instance_method_with_invalid_fields(
      self, mock_logger_critical: mock.Mock) -> None:
    driver.GChromeDriverInstance.initialize(
        settings.CHROME_DRIVER_ABS_PATH[:settings.CHROME_DRIVER_ABS_PATH.
                                        find('chromedriver')],
        _GetAddArgumentCallingOrder())

    with self.assertRaises(exceptions.WebDriverException):
      _ = driver.GetGlobalChromeDriverInstance()

    mock_logger_critical.assert_called()

  @unittest.skipIf(not os.getuid() == 0, 'Requires root!')
  def test_get_global_chrome_driver_instance_method_when_x_bit_is_off(
      self) -> None:
    original_permissions, _ = utils.RemoveFilePermissions(
        settings.CHROME_DRIVER_ABS_PATH, 'x')

    with self.assertRaises(exceptions.WebDriverException):
      _ = driver.GetGlobalChromeDriverInstance()

    utils.AddFilePermissions(settings.CHROME_DRIVER_ABS_PATH,
                             original_permissions)

  def tearDown(self) -> None:
    driver.DisableGlobalChromeDriverInstance()


class TestDisableGlobalChromeDriverInstanceMethod(unittest.TestCase):

  @utils.IgnoreWarnings(ResourceWarning)
  @mock.patch('selenium.webdriver.Chrome.quit')
  def test_disable_global_chromedriver_instance_method(
      self, mock_quit: mock.Mock) -> None:
    driver.GChromeDriverInstance.initialize(settings.CHROME_DRIVER_ABS_PATH,
                                            _GetAddArgumentCallingOrder())
    driver_ = driver.GetGlobalChromeDriverInstance()
    self.assertIsInstance(driver_, webdriver.Chrome)
    self.assertEqual(driver_, driver._DRIVER.driver)  # pylint: disable=protected-access
    driver.DisableGlobalChromeDriverInstance()
    mock_quit.assert_called()
    self.assertIsNone(driver._DRIVER.driver)  # pylint: disable=protected-access

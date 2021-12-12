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

from typing import List

import unittest

from unittest import mock
from selenium import webdriver
from selenium.common import exceptions

from lib import utils
from linkedin import (driver, settings)


class TestPrivateDriverClass(unittest.TestCase):  # pylint: disable=missing-class-docstring

  def setUp(self) -> None:
    self.driver = driver._Driver()  # pylint: disable=protected-access

  def _get_add_argument_calling_order(self) -> List[str]:
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

  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_set_to_none(
      self, mock_add_argument: mock.Mock) -> None:
    if not utils.Which('chromedriver'):
      self.skipTest(
          ('Chromedriver executable is not present in the environment PATH.\n'
           'Check if the x bit is OK in case environment PATH exists.'))
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

  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_set_to_none_but_options_given(
      self, mock_add_argument: mock.Mock) -> None:
    if not utils.Which('chromedriver'):
      self.skipTest(
          ('Chromedriver executable is not present in the environment PATH.\n'
           'Check if the x bit is OK in case environment PATH exists.'))
    try:
      self.driver.enable_webdriver_chrome(
          settings.CHROME_DRIVER_ABS_PATH,
          self._get_add_argument_calling_order())
      mock_add_argument.assert_has_calls([
          mock.call(option)
          for option in self._get_add_argument_calling_order()
      ])
    except exceptions.WebDriverException as exc:
      self.fail(
          'enable_webdriver_chrome(%(path)s, %(opts)s) failed with %(msg)s.' % {
              'path': settings.CHROME_DRIVER_ABS_PATH,
              'opts': self._get_add_argument_calling_order(),
              'msg': str(exc)
          })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '
           '%(type)s') % {'type': utils.Type(self.driver.driver)})

  @mock.patch('selenium.webdriver.ChromeOptions.add_argument')
  def test_enable_webdriver_chrome_with_path_and_options(
      self, mock_add_argument: mock.Mock) -> None:
    try:
      self.driver.enable_webdriver_chrome(
          settings.CHROME_DRIVER_ABS_PATH,
          self._get_add_argument_calling_order())
      mock_add_argument.assert_has_calls([
          mock.call(option)
          for option in self._get_add_argument_calling_order()
      ])
    except exceptions.WebDriverException as exc:
      self.fail(
          'enable_webdriver_chrome(%(path)s, %(opts)s) failed with %(msg)s.' % {
              'path': settings.CHROME_DRIVER_ABS_PATH,
              'opts': self._get_add_argument_calling_order(),
              'msg': str(exc)
          })
    else:
      self.assertIsInstance(
          self.driver.driver, webdriver.Chrome,
          ('Expected self.driver.driver to be webdriver.Chrome, received '
           '%(type)s') % {'type': utils.Type(self.driver.driver)})

  def tearDown(self) -> None:
    del self.driver

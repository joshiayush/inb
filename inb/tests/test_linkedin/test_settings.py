# pylint: disable=missing-module-docstring

# Copyright 2021, The inb authors.
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
#     * Neither the name of The inb authors. nor the names of its
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

import sys
import logging
import unittest
import subprocess

from unittest import mock

import lib
from linkedin import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

file_handler = logging.FileHandler(settings.LOG_DIR_PATH / __name__, mode='w')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


class TestProtectedGetGoogleChromeBinaryVersionFunction(unittest.TestCase):  # pylint: disable=missing-class-docstring

  @lib.IgnoreWarnings(ResourceWarning)
  @unittest.skipUnless(sys.platform == 'linux',
                       'Current platform is not linux.  '
                       'This test is supposed to be ran on linux.')
  @mock.patch('subprocess.check_output')
  def test_call_to_subprocess_check_output_in_linux(self,
                                                    mk_check_output: mock.Mock):
    """This should test if the call to `subprocess.check_output()` method are
    made with the expected commands or not.  This test is particularly aimed for
    `linux` platform so should not run in any other platform.
    """
    _ = settings._GetGoogleChromeBinaryVersion()  # pylint: disable=protected-access

    chrome_binaries = ['google-chrome', 'google-chrome-stable']
    for chrome_binary in chrome_binaries:
      # This is expected to be called at least once with either of the above
      # values or both.  This call in function
      # `settings._GetGoogleChromeBinaryVersion()` finds the path of the Chrome
      # binary present in the system.
      mk_check_output.assert_any_call(['whereis', '-b', chrome_binary])

    chrome_binary_path = []
    for binary in chrome_binaries:
      try:
        chrome_binary_path.append(
            subprocess.check_output(['whereis', '-b',
                                     binary]).decode('utf-8')[len(binary) +
                                                              1::].strip())
      except subprocess.CalledProcessError as exc:
        logger.error(('CalledProcessError: Exit code %d.'
                      '\n%s.'), exc.returncode, exc.output)
        continue
    for i in range(len(chrome_binary_path)):
      if chrome_binary_path[i] == '':
        chrome_binary_path = chrome_binary_path[0:i:] + chrome_binary_path[i +
                                                                           1::]

    for path in chrome_binary_path:
      # This is expected to be called at least once with any of the collected
      # path above or all.  This call in function
      # `settings._GetGoogleChromeBinaryVersion()` finds the actual Chrome
      # version.
      mk_check_output.assert_any_call([path, '--version'])

  @lib.IgnoreWarnings(ResourceWarning)
  @unittest.skipUnless(sys.platform == 'darwin',
                       'Current platform is not darwin.  '
                       'This test is supposed to be ran on darwin.')
  @mock.patch('subprocess.check_output')
  def test_call_to_subprocess_check_output_in_darwin(
      self, mk_check_output: mock.Mock):
    """This should test if the call to `subprocess.check_output()` method are
    made with the expected commands or not.  This test is particularly aimed for
    `darwin` platform so should not run in any other platform.
    """
    chrome_binary_path = (
        r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')

    for path in chrome_binary_path:
      # This is expected to be called at least once with any of the collected
      # path above or all.  This call in function
      # `settings._GetGoogleChromeBinaryVersion()` finds the actual Chrome
      # version.
      mk_check_output.assert_any_call([path, '--version'])

  @lib.IgnoreWarnings(ResourceWarning)
  @unittest.skipUnless(sys.platform in ('win32', 'cygwin'),
                       'Current platform is not win32 or cygwin.  '
                       'This test is supposed to be ran on win32 or cygwin.')
  @mock.patch('subprocess.check_output')
  def test_call_to_subprocess_check_output_in_win32_or_cygwin(
      self, mk_check_output: mock.Mock):
    """This should test if the call to `subprocess.check_output()` method are
    made with the expected commands or not.  This test is particularly aimed for
    `win32` or `cygwin` platform so should not run in any other platform.
    """
    chrome_binary_path = (
        r'%ProgramFiles%\Google\Chrome\Application\chrome.exe',
        r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe',
        r'%LocalAppData%\Google\Chrome\Application\chrome.exe',
        r'C:\Users\USER\AppData\Local\Google\Chrome\Application\chrome.exe')

    for path in chrome_binary_path:
      # This is expected to be called at least once with any of the collected
      # path above or all.  This call in function
      # `settings._GetGoogleChromeBinaryVersion()` finds the actual Chrome
      # version.
      mk_check_output.assert_any_call([
          'wmic', 'datafile', 'where', f'name={path}', 'get', 'Version',
          '/value'
      ])


class TestProtectedCheckIfChromeDriverIsCompatibleWithGoogleChromeInstalledFunction(  # pylint: disable=line-too-long, missing-class-docstring
    unittest.TestCase):

  def test_if_function_returns_true(self):
    """This should test if the function
    `_CheckIfChromeDriverIsCompatibleWithGoogleChromeInstalled` actually returns `True`
    in case where the actual chrome binary present has a version equals to
    `settings._GOOGLE_CHROME_COMPATIBLE_VERSION_WITH_INSTALLED_CHROMEDRIVER`.
    """
    if settings._GetGoogleChromeBinaryVersion(  # pylint: disable=protected-access
    ) != settings._GOOGLE_CHROME_COMPATIBLE_VERSION_WITH_INSTALLED_CHROMEDRIVER:  # pylint: disable=protected-access
      self.skipTest(
          'There seems to be an update in the Google Chrome version you are currently '
          'running in your system due to which this test will fail because of the '
          'variable `settings._GOOGLE_CHROME_COMPATIBLE_VERSION_WITH_INSTALLED_CHROMEDRIVER` '
          'which has a concrete version value for Google Chrome binary, so it is better to '
          'skip this test rather having a failure.')
    self.assertTrue(
        settings._CheckIfChromeDriverIsCompatibleWithGoogleChromeInstalled())  # pylint: disable=protected-access


class TestProtectedGetPlatformSpecificChromeDriverCompatibleVersionUrlFunction(  # pylint: disable=missing-module-docstring
    unittest.TestCase):
  _CHROME_DRIVER_BINARY_RELEASE = (
      '95.0.4638.69',
      '96.0.4664.45',
      '97.0.4692.36',
  )
  _CHROME_DRIVER_STORAGE_GOOGLEAPIS = 'https://chromedriver.storage.googleapis.com'  # pylint: disable=line-too-long

  @unittest.skipUnless(sys.platform == 'linux',
                       'Current platform is not linux.  '
                       'This test is supposed to be ran on linux.')
  def test_function_return_value_in_linux(self):
    # Make a Google Chrome version string from the
    # `self._CHROME_DRIVER_BINARY_RELEASE` as Google Chrome version.  This tuple
    # will contain every possible version major the function
    # `settings._GetPlatformSpecificChromeDriverCompatibleVersionUrl()` can get
    # called with.
    for release in self._CHROME_DRIVER_BINARY_RELEASE:
      self.assertEqual(
          settings._GetPlatformSpecificChromeDriverCompatibleVersionUrl(  # pylint: disable=protected-access
              release),
          f'{self._CHROME_DRIVER_STORAGE_GOOGLEAPIS}/{release}/{settings._CHROME_DRIVER_BINARY}_linux64.zip'  # pylint: disable=protected-access, line-too-long
      )

  @unittest.skipUnless(sys.platform == 'darwin',
                       'Current platform is not darwin.  '
                       'This test is supposed to be ran on darwin.')
  def test_function_return_value_in_darwin(self):
    # Make a Google Chrome version string from the
    # `self._CHROME_DRIVER_BINARY_RELEASE` as Google Chrome version.  This tuple
    # will contain every possible version major the function
    # `settings._GetPlatformSpecificChromeDriverCompatibleVersionUrl()` can get
    # called with.
    for release in self._CHROME_DRIVER_BINARY_RELEASE:
      self.assertEqual(
          settings._GetPlatformSpecificChromeDriverCompatibleVersionUrl(  # pylint: disable=protected-access
              release),
          f'{self._CHROME_DRIVER_STORAGE_GOOGLEAPIS}/{release}/{settings._CHROME_DRIVER_BINARY}_mac64.zip'  # pylint: disable=protected-access, line-too-long
      )

  @unittest.skipUnless(sys.platform in ('win32', 'cygwin'),
                       'Current platform is not win32 or cygwin.  '
                       'This test is supposed to be ran on win32 or cygwin.')
  def test_function_return_value_in_win32_or_cygwin(self):
    # Make a Google Chrome version string from the
    # `self._CHROME_DRIVER_BINARY_RELEASE` as Google Chrome version.  This tuple
    # will contain every possible version major the function
    # `settings._GetPlatformSpecificChromeDriverCompatibleVersionUrl()` can get
    # called with.
    for release in self._CHROME_DRIVER_BINARY_RELEASE:
      self.assertEqual(
          settings._GetPlatformSpecificChromeDriverCompatibleVersionUrl(  # pylint: disable=protected-access
              release),
          f'{self._CHROME_DRIVER_STORAGE_GOOGLEAPIS}/{release}/{settings._CHROME_DRIVER_BINARY}_win32.zip'  # pylint: disable=protected-access, line-too-long
      )

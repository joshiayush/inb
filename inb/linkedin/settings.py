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

import re
import os
import sys
import logging
import pathlib
import subprocess

LOG_DIR_PATH = pathlib.Path(__file__).resolve().parent.parent.parent / 'logs'

# Variable's value decides whether logging to stream is allowed in the entire
# project.
#
# Note: You must not update the value of this variable directly, you must call
# the `TurnOnLoggingLevelDebug()` function to update its value otherwise you may
# update the value of this variable but this particular module will not have any
# effect of that change.
LOGGING_TO_STREAM_ENABLED = False

# We want to create the log directory if it does not exists otherwise the file
# handlers for loggers used in other modules will complain about its absence.
if not os.path.exists(LOG_DIR_PATH):
  os.mkdir(LOG_DIR_PATH)

LOG_FORMAT_STR = '%(asctime)s:%(name)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s'  # pylint: disable=line-too-long

INB_VERSION = '1.0.0'

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler(LOG_DIR_PATH / __name__, mode='w')
file_handler.setFormatter(logging.Formatter(LOG_FORMAT_STR))

logger.addHandler(file_handler)


def TurnOnLoggingToStream() -> None:
  global LOGGING_TO_STREAM_ENABLED
  LOGGING_TO_STREAM_ENABLED = True
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(LOG_FORMAT_STR))
  logger.addHandler(stream_handler)


_CHROME_BINARY_NOT_FOUND_MSG = 'Google Chrome binary is not present in path %s.'
_CHROME_BINARIES_NOT_FOUND_MSG = (
    'Google Chrome binary is not present in the following paths\n'
    '%s')


def _GetGoogleChromeBinaryVersion() -> str:
  version_regex = r'[0-9]{2}.[0-9]{1}.[0-9]{4}.[0-9]{2}'
  if sys.platform == 'linux':
    chrome_binaries = ['google-chrome', 'google-chrome-stable']
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
      try:
        version = subprocess.check_output([path, '--version']).decode('utf-8')
      except subprocess.CalledProcessError:
        logger.error(_CHROME_BINARY_NOT_FOUND_MSG, path)
        continue
      else:
        version = re.search(version_regex, version)
        return version.group(0)
    raise FileNotFoundError(_CHROME_BINARIES_NOT_FOUND_MSG %
                            (', '.join(chrome_binary_path)))
  elif sys.platform == 'darwin':
    chrome_binary_path = (
        r'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    for path in chrome_binary_path:
      try:
        version = subprocess.check_output([path, '--version']).decode('utf-8')
      except subprocess.CalledProcessError:
        logger.error(_CHROME_BINARY_NOT_FOUND_MSG, path)
        continue
      else:
        version = re.search(version_regex, version)
        return version.group(0)
    raise FileNotFoundError(_CHROME_BINARIES_NOT_FOUND_MSG %
                            (', '.join(chrome_binary_path)))
  elif sys.platform in ('win32', 'cygwin'):
    chrome_binary_path = (
        r'%ProgramFiles%\Google\Chrome\Application\chrome.exe',
        r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe',
        r'%LocalAppData%\Google\Chrome\Application\chrome.exe',
        r'C:\Users\USER\AppData\Local\Google\Chrome\Application\chome.exe')
    for path in chrome_binary_path:
      try:
        version = subprocess.check_output([
            'wmic', 'datafile', 'where', f'name={path}', 'get', 'Version',
            '/value'
        ]).decode('utf-8')
      except subprocess.CalledProcessError:
        logger.error(_CHROME_BINARY_NOT_FOUND_MSG, path)
        continue
      else:
        version = re.search(version_regex, version)
        return version.group(0)
    raise FileNotFoundError(_CHROME_BINARIES_NOT_FOUND_MSG %
                            (', '.join(chrome_binary_path)))


def ChromeDriverAbsPath() -> str:
  dir_path = os.path.dirname(os.path.abspath(__file__))
  last_inb_indx = dir_path.rfind('inb')
  return os.path.join(dir_path[:last_inb_indx], 'driver/chromedriver')


def GetLinkedInUrl() -> str:
  return 'https://www.linkedin.com'


def GetLinkedInLoginPageUrl() -> str:
  return GetLinkedInUrl() + '/login/'


def GetLinkedInMyNetworkPageUrl() -> str:
  return GetLinkedInUrl() + '/mynetwork/'

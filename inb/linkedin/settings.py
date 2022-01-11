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
import click
import pathlib
import logging
import subprocess

from urllib import (request, parse)

try:
  from gettext import gettext as _  # pylint: disable=unused-import
except ImportError:
  _ = lambda msg: msg

CONNECTION_LIMIT_EXCEED_EXCEPTION_MESSAGE = """Invalid connection limit %d.
LinkedIn does not allow to send over 80 invitations per-day to a non-premium
account.
Please be patient and make sure that the connection limit is between (0, 80]
and you are not running the bot in a day more than once otherwise LinkedIn
will block your IP."""

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

LOG_FORMAT_STR = '%(asctime)s:%(name)s:%(levelname)s:%(funcName)s\n%(message)s'  # pylint: disable=line-too-long

INB_VERSION = '1.0.0'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_DIR_PATH / __name__, mode='a')
file_handler.setFormatter(logging.Formatter(LOG_FORMAT_STR))

logger.addHandler(file_handler)


def TurnOnLoggingToStream() -> None:
  global LOGGING_TO_STREAM_ENABLED
  LOGGING_TO_STREAM_ENABLED = True
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(LOG_FORMAT_STR))
  logger.addHandler(stream_handler)


_CHROME_BINARY_NOT_FOUND_MSG = _('Google Chrome binary is not present in path %s.')
_CHROME_BINARIES_NOT_FOUND_MSG = _(
    'Google Chrome binary is not present in the following paths\n'
    '%s')

_CHROME_DRIVER_BINARY = 'chromedriver'
_CHROME_DRIVER_ZIP_FILE = None

# Chromedriver that comes with the repository is only compatible with the Google
# Chrome version _GOOGLE_CHROME_COMPATIBLE_VERSION_WITH_INSTALLED_CHROMEDRIVER.
#
# This version must be changed with the installed 'chromedriver' version that
# comes with the repository.
_GOOGLE_CHROME_COMPATIBLE_VERSION_WITH_INSTALLED_CHROMEDRIVER = '97.0.4692.71'


def _ExtractChromeDriverZip(chromedriver_zip: str) -> None:
  """Utility routine to `unzip` the downloaded `chromedriver` archive present
  at path `chromedriver_zip`.

  This function will extract all the contents of `chromedriver` archive in the
  same directory where the archive is installed.

  Args:
    chromedriver_zip: `Chromedriver` archive file path.
  """
  import zipfile  # pylint: disable=import-outside-toplevel
  driver_dir = pathlib.PurePath(chromedriver_zip).parent
  with zipfile.ZipFile(chromedriver_zip, 'r') as zip_f:
    zip_f.extractall(driver_dir)


def _RetrieveChromeDriverZip(url: str, dest: str, verbose: bool = True) -> str:
  """Utility function to download `chromedriver` zip file at the specified URL.

  Utility function to download and store `chromedriver` zip file in the
  destination `dest`.  This function also sets the value of
  `_CHROME_DRIVER_ZIP_FILE` variable equals to the `chromedriver` zip file name
  at the specified URL so to later use the archive file name to extract the
  `chromedriver` executable from it.

  Args:
    url: URL to download the file from.
    dest: Destination where to place the file after downloading.
    verbose: If `True` shows the downloading status.

  Returns:
    Destination where the file is placed after installing.
  """
  u = request.urlopen(url)

  scheme, netloc, path, query, fragment = parse.urlsplit(url)  # pylint: disable=unused-variable
  filename = os.path.basename(path)
  if not filename:
    filename = 'downloaded'
  global _CHROME_DRIVER_ZIP_FILE
  _CHROME_DRIVER_ZIP_FILE = filename
  if dest:
    filename = os.path.join(dest, filename)

  with open(filename, 'wb') as f:
    if verbose:
      meta = u.info()
      if hasattr(meta, 'getheaders'):
        meta_func = meta.getheaders
      else:
        meta_func = meta.get_all
      meta_length = meta_func('Content-Length')
      file_size = None
      if meta_length:
        file_size = int(meta_length[0])
        click.echo(_('Downloading: %s Bytes: %s') % (url, file_size))

    file_size_dl = 0
    block_size = 8192
    while True:
      buffer = u.read(block_size)
      if not buffer:
        break

      file_size_dl += len(buffer)
      f.write(buffer)

      if verbose:
        status = '{0:16}'.format(file_size_dl)  # pylint: disable=consider-using-f-string
        if file_size:
          status += '   [{0:6.2f}%]'.format(file_size_dl * 100 / file_size)  # pylint: disable=consider-using-f-string
        status += chr(13)
        click.echo(f'{status}\r', None, False)
    if verbose:
      click.echo('')

  return filename


def _GetGoogleChromeBinaryVersion() -> str:
  """Returns the `Google Chrome` version the user is using in its system.

  This function returns the `Google Chrome` version independent of the platform
  the user is running.  This function creates a child process using `subprocess`
  module to talk to the shell and retrieve the `Google Chrome` version present
  in the system.

  This function checks the following locations where the `Google Chrome`
  executable could be present in user's system.

  * `Linux`

    On `linux` platform this function checks if the binary `google-chrome` and
    `google-chrome-stable` is present, if yes this function in its child process
    will provide a flag `--version` to the `Google Chrome` binary present in
    order to retrieve the version string.

    The child process calls for `linux` platform looks something like the
      following:

    * If `google-chrome` is present.

  ```shell
  google-chrome --version
  ```

    * If `google-chrome` is not present.

  ```shell
  google-chrome-stable --version
  ```

  * `MacOS`

    On `MacOs` platform this function will create a child process and will
    provide `--version` flag to the `Google Chrome` executable present in the
    path `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`.

    The child process call for `linux` platform looks something like the
      following:

  ```shell
  /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --version
  ```

    @TODO(joshiayush): Find alternative paths on `MacOS`.

  * `Windows`

    God forbid if you are on `Windows` because there is no tested version of
    this function on `Windows` but so far what we've come up with is the
    following:

    This function will search for the `Google Chrome` executable in the
    following paths:

  ```python
  chrome_binary_path = (
      '%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe',
      '%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe',
      '%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Users\\USER\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'
  )
  ```

    and will try to execute the following commands in its child process to
    retrieve the `Google Chrome` version.

  ```shell
  wmic datafile where name=${path} get Version /value
  ```

    where path is the `element` of `chrome_binary_path` tuple on `Windows`.

  Returns:
    `Google Chrome` version.
  """
  version_regex = r'[0-9]{1,2}.[0-9]{1}.[0-9]{1,4}.[0-9]{1,3}'
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
        r'C:\Users\USER\AppData\Local\Google\Chrome\Application\chrome.exe')
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


def _CheckIfChromeDriverIsCompatibleWithGoogleChromeInstalled() -> str:
  """Checks if the `chromedriver` that comes with the `inb` repository is
  compatible with the `Google Chrome` version the user is using in its system.

  This function checks if the `Google Chrome` version the user is using in its
  system matches against the `Google Chrome` version supported by `chromedriver`
  that comes with the `inb` repository which is
  `_GOOGLE_CHROME_COMPATIBLE_VERSION_WITH_INSTALLED_CHROMEDRIVER`.

  Returns:
    True if the `chromedriver` is compatible with the `Google Chrome` installed.
  """
  google_chrome_version = _GetGoogleChromeBinaryVersion()
  if google_chrome_version == _GOOGLE_CHROME_COMPATIBLE_VERSION_WITH_INSTALLED_CHROMEDRIVER:  # pylint: disable=line-too-long
    return True
  return False


def _GetPlatformSpecificChromeDriverUrlForGoogleChromeMajor(major: str) -> str:
  """Returns the platform specific `chromedriver` version that is compatible
  with the `Google Chrome` major given as `major`.

  This function only supports `Google Chrome` major that is present in the
  following list of `chromedriver` releases:

  ```python
  (
    '95.0.4638.69',
    '96.0.4664.45',
    '97.0.4692.36',
  )
  ```

  `Google Chrome` version against a major that is not present in the above list
  will not receive a compatible version of `chromedriver` through this function.

  Args:
    major: `Google Chrome` major.

  Returns:
    Platform specific `chromedriver` file URL that is compatible with
      `Google Chrome` with the give `major` as major.
  """
  chromedriver_storage_googleapis = 'https://chromedriver.storage.googleapis.com'  # pylint: disable=line-too-long
  for release in (
      '95.0.4638.69',
      '96.0.4664.45',
      '97.0.4692.36',
  ):
    if release.startswith(major):
      if sys.platform == 'linux':
        return f'{chromedriver_storage_googleapis}/{release}/{_CHROME_DRIVER_BINARY}_linux64.zip'  # pylint: disable=line-too-long
      elif sys.platform == 'darwin':
        return f'{chromedriver_storage_googleapis}/{release}/{_CHROME_DRIVER_BINARY}_mac64.zip'  # pylint: disable=line-too-long
      elif sys.platform in ('win32', 'cygwin'):
        return f'{chromedriver_storage_googleapis}/{release}/{_CHROME_DRIVER_BINARY}_win32.zip'  # pylint: disable=line-too-long


def _GetPlatformSpecificChromeDriverCompatibleVersionUrl(
    google_chrome_version: str) -> str:
  """Returns the platform specific `chromedriver` version URL that is
  compatible with the `Google Chrome` version given as `google_chrome_version`.

  This function takes out the `major` version from the `google_chrome_version`
  string and calls the function
  `_GetPlatformSpecificChromeDriverUrlForGoogleChromeMajor()` with the major
  that we just took out to receive a compatible `chromedriver` version URL.

  Args:
    google_chrome_version: `Google Chrome` version.

  Returns:
    `Chromedriver` version URL that is compatible with the `Google Chrome`
      version given as `google_chrome_version`.
  """
  major_regex = re.compile(r'^[0-9]{2}')
  google_chrome_major = re.search(major_regex, google_chrome_version).group(0)
  return _GetPlatformSpecificChromeDriverUrlForGoogleChromeMajor(
      google_chrome_major)


def _InstallGoogleChromeCompatibleChromeDriver() -> None:
  """Installs `Google Chrome` compatible `chromedriver`.

  This function installs a `Google Chrome` compatible `chromedriver` version.
  Because user's can have different versions of `Google Chrome` installed in
  their system so we need to handle the case where the `chromedriver` that
  comes with the `inb` repository is not compatible with the `Google Chrome`
  version they are using on their system.

  To handle the above case we install the compatible version of `chromedriver`
  from the `googleapis` by calling the function
  `_GetPlatformSpecificChromeDriverCompatibleVersionUrl()` to return the URL
  for `chromedriver` and then later using that URL with function
  `_RetrieveChromeDriverZip()` to install `chromedriver` from `googleapis`.

  Once the `chromedriver` is installed we know that it is in a form of zip so
  we need to extract it and we do so by calling the function
  `_ExtractChromeDriverZip()` with the zip file path.
  """
  _RetrieveChromeDriverZip(
      _GetPlatformSpecificChromeDriverCompatibleVersionUrl(
          _GetGoogleChromeBinaryVersion()),
      True if LOGGING_TO_STREAM_ENABLED else False)
  _ExtractChromeDriverZip(
      os.path.join(_GetInstalledChromeDriverDirectoryPath(),
                   _CHROME_DRIVER_ZIP_FILE))


def _GetInstalledChromeDriverDirectoryPath() -> str:
  """Returns the absolute filesystem path to the directory where `chromedriver`
  that comes with the `inb` repository is installed.

  Returns:
    Absolute filesystem path the `chromedriver` directory.
  """
  dir_path = os.path.dirname(os.path.abspath(__file__))
  last_inb_indx = dir_path.rfind('inb')
  return os.path.join(dir_path[:last_inb_indx:], 'driver')


def ChromeDriverAbsolutePath() -> str:
  """Returns the absolute filesystem path to the `chromedriver` installed inside
  the `driver` directory.

  This function checks if the `chromedriver` that comes with the `inb`
  repository is compatible with the `Google Chrome` installed in the user's
  system; if yes it returns the absolute filesystem path to the `chromedriver`
  installed inside the `driver` directory.

  If the `chromedriver` if not compatible with the `Google Chrome` version the
  user is using in its system then this function tries to install a compatible
  `chromedriver` inside the directory `driver` and if successful, it returns the
  absolute filesystem path to the `chromedriver`.

  Returns:
    Absolute path to `chromedriver`.
  """
  if _CheckIfChromeDriverIsCompatibleWithGoogleChromeInstalled():
    return os.path.join(_GetInstalledChromeDriverDirectoryPath(),
                        _CHROME_DRIVER_BINARY)
  _InstallGoogleChromeCompatibleChromeDriver()
  return os.path.join(_GetInstalledChromeDriverDirectoryPath(),
                      _CHROME_DRIVER_BINARY)


def GetLinkedInUrl() -> str:
  """Returns URL to LinkedIn."""
  return 'https://www.linkedin.com'


def GetLinkedInLoginPageUrl() -> str:
  """Returns URL to LinkedIn's login page."""
  return GetLinkedInUrl() + '/login/'


def GetLinkedInMyNetworkPageUrl() -> str:
  """Returns URL to LinkedIn's `MyNetwork` page."""
  return GetLinkedInUrl() + '/mynetwork/'

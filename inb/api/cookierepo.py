# Copyright 2023 The inb Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Authentication Cookie-Repository Management Package."""

import os
import time
import pickle
import pathlib

from requests import cookies

from api import settings, exceptions as linkedin_api_exceptions


class CookieRepository(object):
  """Creates a 'Cookie Repository' in the given directory."""

  def __init__(self, username: str, cookies_: cookies.RequestsCookieJar,
               cookie_dir: str) -> None:
    self.cookies = cookies_
    self.username = username

    if cookie_dir is None:
      cookie_dir = settings.INB_COOKIE_DIR
    self.cookie_dir = pathlib.Path(cookie_dir)

  def get_cookie_dir(self) -> str:
    """Returns a 'fs' compatible path of the cookie directory."""
    return os.fspath(self.cookie_dir)

  def _get_cookies_jar_file_path(self) -> pathlib.Path:
    """Returns the cookies jar file path that is generated after combining the
    given cookie directory with the label 'username'.

    Returns:
      Cookies jar file path.
    """
    return self.cookie_dir / self.username

  def save(self) -> None:
    """Saves the constructor initialized cookies in the constructor initialized
    cookies directory path.
    """
    if not os.path.exists(os.fspath(self.cookie_dir)):
      os.makedirs(os.fspath(self.cookie_dir))

    # Every user has a Cookie Repository in the 'cookies directory' with a file
    # name equal to their 'username'.
    cookie_jar_file_path = self._get_cookies_jar_file_path()
    with open(cookie_jar_file_path, 'wb') as jar_file:
      pickle.dump(self.cookies, jar_file)

  def get_cookies(self) -> cookies.RequestsCookieJar:
    """Returns the 'RequestCookieJar' instance of the cookies saved in the
    cookies directory for the instantiated username.

    Returns:
      'cookies.RequestsCookieJar' instance of user cookies.
    """
    # Every user has a Cookie Repository in the 'cookies directory' with a file
    # name equal to their 'username'.
    cookie_jar_file_path = self._get_cookies_jar_file_path()
    if not os.path.exists(cookie_jar_file_path):
      return None

    cookies_ = None
    with open(cookie_jar_file_path, 'rb') as jar_file:
      cookies_ = pickle.load(jar_file)

    # We still need to check if the cookies have expired.
    for cookie in cookies_:
      if cookie.name == 'JSESSIONID' and cookie.value:
        if cookie.expires and cookie.expires > time.time():
          raise linkedin_api_exceptions.LinkedInSessionExpiredException()
        break
    return cookies_

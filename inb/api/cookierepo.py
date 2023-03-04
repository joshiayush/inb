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

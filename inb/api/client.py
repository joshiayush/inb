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
"""Client simulator for Voyager API."""

import sys
import bs4
import json
import logging
import requests

from requests import cookies

from api import (exceptions as linkedin_api_exceptions, cookierepo, settings)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(settings.INB_LOG_DIR / __name__, mode='a')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)


class Client(object):
  """Client simulator for Voyager API."""

  LINKEDIN_BASE_URL = 'https://www.linkedin.com'
  LINKEDIN_AUTH_URL = f'{LINKEDIN_BASE_URL}/uas/authenticate'
  VOYAGER_API_BASE_URL = f'{LINKEDIN_BASE_URL}/voyager/api'

  API_REQUEST_HEADERS = {
      'user-agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                     ' AppleWebKit/537.36 (KHTML, like Gecko)'
                     ' Chrome/110.0.0.0 Safari/537.36'),
      'accept-language': 'en-AU,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
      'x-li-lang': 'en_US',
      'x-restli-protocol-version': '2.0.0'
  }

  API_AUTH_REQUEST_HEADERS = {
      'X-Li-User-Agent':
          'LIAuthLibrary:3.2.4 com.linkedin.LinkedIn:8.8.1 iPhone:8.3',
      'User-Agent':
          'LinkedIn/8.8.1 CFNetwork/711.3.18 Darwin/14.0.0',
      'X-User-Language':
          'en',
      'X-User-Locale':
          'en_US',
      'Accept-Language':
          'en-us',
  }

  def __init__(self,
               *,
               debug: bool = False,
               refresh_cookies: bool = False,
               proxies: dict = None,
               cookies_dir: str = None) -> None:
    self.session = requests.session()

    if not proxies:
      proxies = {}
    self.session.proxies.update(proxies)
    self.session.headers.update(Client.API_REQUEST_HEADERS)

    self.logger = logger
    self.proxies = proxies
    self.metadata = {}

    self._cookies_dir = cookies_dir
    self._use_cookie_cache = not refresh_cookies

    self._logger = logger
    if not debug:
      self._logger.setLevel(logging.CRITICAL)

  def _set_session_cookies(self, cookies_: cookies.RequestsCookieJar) -> None:
    """Sets the session cookies for authentication with voyager API."""
    self.session.cookies = cookies_
    self.session.headers['csrf-token'] = self.session.cookies.get(
        'JSESSIONID').strip('"')

  def _request_session_cookies(self) -> cookies.RequestsCookieJar:
    """Request cookies for the established session."""
    return requests.get(Client.LINKEDIN_AUTH_URL,
                        headers=Client.API_AUTH_REQUEST_HEADERS,
                        proxies=self.proxies,
                        timeout=60.0).cookies

  def _fetch_metadata(self) -> None:
    result_ = requests.get(Client.LINKEDIN_BASE_URL,
                           cookies=self.session.cookies,
                           headers=Client.API_AUTH_REQUEST_HEADERS,
                           proxies=self.proxies,
                           timeout=60.0)
    soup_ = bs4.BeautifulSoup(result_.text, 'lxml')

    if client_application_instance_raw := soup_.find(
        'meta', attrs={'name': 'applicationInstance'}):
      client_application_instance = json.loads(
          client_application_instance_raw.attrs.get('content') or {})
      self.metadata['clientApplicationInstance'] = client_application_instance

    if client_page_instance_id_raw := soup_.find(
        'meta', attrs={'name': 'clientPageInstanceId'}):
      client_page_instance_id = client_page_instance_id_raw.attrs.get(
          'content') or {}
      self.metadata['clientPageInstanceId'] = client_page_instance_id

  def _fallback_authentication(self, username: str, password: str) -> None:
    self._set_session_cookies(self._request_session_cookies())

    payload_ = {
        'session_key': username,
        'session_password': password,
        'JSESSIONID': self.session.cookies['JSESSIONID']
    }
    result_ = requests.post(Client.LINKEDIN_AUTH_URL,
                            data=payload_,
                            cookies=self.session.cookies,
                            headers=Client.API_AUTH_REQUEST_HEADERS,
                            proxies=self.proxies,
                            timeout=60.0)
    data_ = result_.json()
    if data_ and data_['login_result'] != 'PASS':
      raise linkedin_api_exceptions.LinkedInChallengeException(
          data_['login_result'])
    if result_.status_code == 401:
      raise linkedin_api_exceptions.LinkedInUnauthorizedException()
    if result_.status_code != 200:
      raise linkedin_api_exceptions.LinkedInUnexpectedStatusException(
          f'Received "{result_.status_code}" as a status code for'
          f' payload "{repr(payload_)}"')

    self._set_session_cookies(result_.cookies)
    self._cookie_repository.cookies = result_.cookies
    self._cookie_repository.username = username
    self._cookie_repository.save()

  def authenticate(self, username: str, password: str) -> None:
    self._cookie_repository = cookierepo.CookieRepository(
        username=username, cookies_=None, cookie_dir=self._cookies_dir)
    if self._use_cookie_cache:
      self._logger.debug('Attempting to use cached cookies at %s',
                         self._cookie_repository.get_cookie_dir())
      cookies_ = self._cookie_repository.get_cookies()
      if cookies_:
        self._set_session_cookies(cookies_)
        self._fetch_metadata()
        return

    self._logger.warning('Empty cookie repository at %s',
                         self._cookie_repository.get_cookie_dir())
    self._logger.info(
        'Falling back to authentication using (username="%s", password="%s")',
        username, '*' * len(password))

    self._fallback_authentication(username, password)
    self._fetch_metadata()

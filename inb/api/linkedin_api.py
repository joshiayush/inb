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
"""API to send data to Voyager end-points and trigger actions accordingly."""

from __future__ import annotations

from typing import Callable

import sys
import json
import time
import random
import logging
import requests
import operator

from requests import cookies
from urllib.parse import urlencode

from api import client, settings
from api.utils import utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(settings.INB_LOG_DIR / __name__, mode='a')
file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))

if settings.LOGGING_TO_STREAM_ENABLED:
  stream_handler = logging.StreamHandler(sys.stderr)
  stream_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT_STR))
  logger.addHandler(stream_handler)

logger.addHandler(file_handler)


def default_evade() -> None:
  """Sleeps for a random amount of time in bound (2,5)."""
  time.sleep(random.randint(2, 5))


class LinkedIn(object):
  """API creating an interface between `LinkedIn Voyager API` and `inb`."""

  MAX_SEARCH_COUNT = 49

  _MAX_REPEATED_REQUEST = 200

  def __init__(self,
               username: str,
               password: str,
               /,
               *,
               authenticate: bool = True,
               refresh_cookies: bool = False,
               debug: bool = False,
               proxies: dict = None,
               cookies_: cookies.RequestsCookieJar = None,
               cookies_dir: str = None) -> None:
    """Initializes a LinkedIn client for the Voyager API.
    
    This client allows you to interact with LinkedIn's Voyager API, which
    provides access to LinkedIn data such as search results, profile data,
    and more. Once initialized, the client can be used to make API requests
    to LinkedIn.

    Client need not to authenticate repeatedly once the authentication cookies
    are set in the very first authentication routine, but in any case the
    authentication fails, fallback to the normal authentication by setting the
    `authentication` to `True`. Alternatively, you can pass in an existing
    `cookies.RequestsCookieJar` object using the `cookies_` parameter, which
    will bypass the authentication process. Note that if the authentication
    fails, the client will fallback to the normal authentication by setting
    the `authentication` parameter to `True`.

    If you encounter a `LinkedInSessionExpiredException`, you can re-claim new
    cookies from LinkedIn's authentication server by setting the
    `refresh_cookies` parameter to `True`.

    Args:
      username:        Your LinkedIn username.
      password:        Your LinkedIn password.
      authenticate:    Whether to authenticate with LinkedIn. Defaults to True.
      refresh_cookies: Whether to refresh the authentication cookies if the
                       authentication fails. Defaults to False.
      debug:           Whether to enable debug logging. Defaults to False.
      proxies:         A dictionary of proxy settings. Defaults to None.
      cookies_:        An existing cookie jar to use for authentication.
                       Defaults to None.
      cookies_dir:     The directory to store authentication cookies in.
                       Defaults to None.
    """
    self.client = client.Client(debug=debug,
                                refresh_cookies=refresh_cookies,
                                proxies=proxies,
                                cookies_dir=cookies_dir)

    self._logger = logger
    if not debug:
      self._logger.setLevel(logging.CRITICAL)

    if authenticate:
      if cookies_:
        self.client._set_session_cookies(cookies_)
      else:
        self.client.authenticate(username=username, password=password)

  def _fetch(self,
             uri: str,
             evade: Callable = default_evade,
             base_request: bool = False,
             **kwargs) -> requests.Response:
    """Performs an HTTP GET request to the LinkedIn Voyager API or to the
    LinkedIn website.

    The request URL is obtained by concatenating the `uri` argument with the
    LinkedIn API base URL (`VOYAGER_API_BASE_URL`) or with the LinkedIn
    website base URL (`LINKEDIN_BASE_URL`), depending on the value of the
    `base_request` argument.

    The `evade` function is called before performing the request, to avoid
    being detected as a bot.

    Any additional keyword arguments are passed to the `requests.Session.get`
    method.

    Args:
      uri:          The path to append to the base URL to obtain the request
                    URL.
      evade:        A function that takes no arguments and is called before
                    performing the request to avoid being detected as a bot.
                    Defaults to `default_evade`.
      base_request: Whether the request should be sent to the LinkedIn Voyager
                    API (False) or to the LinkedIn website (True). Defaults to
                    False.
      **kwargs:     Any additional keyword arguments are passed to the
                    `requests.Session.get` method.

    Returns:
      The HTTP response object.
    """
    evade()
    if not base_request:
      url = self.client.VOYAGER_API_BASE_URL
    else:
      url = self.client.LINKEDIN_BASE_URL
    url = f'{url}{uri}'
    return self.client.session.get(url, **kwargs)

  def _post(self,
            uri: str,
            evade: Callable = default_evade,
            base_request: bool = False,
            **kwargs):
    """Sends a POST request to the LinkedIn API.

    This method sends an HTTP POST request to the LinkedIn API endpoint
    specified by the given URI. The request is made using the session object
    managed by the LinkedIn client. The URL for the request is constructed by
    concatenating the LinkedIn API base URL and the given URI. The optional
    `evade` parameter can be used to specify a function that should be called
    before making the request to evade detection by LinkedIn.

    Args:
      uri:          The URI path of the LinkedIn API endpoint to request.
      evade:        A function to be called before making the
                    request to evade detection. Defaults to `default_evade`.
      base_request: If `True`, the URL for the request will
                    be constructed using the LinkedIn base URL instead of the
                    API base URL. Defaults to `False`.
      **kwargs:     Any additional keyword arguments are passed directly to the
                    `requests.post` method.

    Returns:
      The HTTP response returned by the server.
    """
    evade()
    if not base_request:
      url = self.client.VOYAGER_API_BASE_URL
    else:
      url = self.client.LINKEDIN_BASE_URL
    url = f'{url}{uri}'
    return self.client.session.post(url, **kwargs)

  def search(self, params: dict, limit: int = -1, offset: int = 0) -> list:
    """Performs a search on LinkedIn with given parameters and returns the
    results.

    Args:
      params: Dictionary of parameters for the search query.
      limit:  Maximum number of results to return. Defaults to -1 (i.e.,
              return all results).
      offset: Number of results to skip before returning results. Defaults
              to 0.

    Returns:
      A list of search results in JSON format, with each element representing
      a profile or company that matches the search criteria.
    """
    count_ = LinkedIn.MAX_SEARCH_COUNT
    limit = -1 if limit is None else limit

    results_ = []
    while True:
      if limit > -1 and limit - len(results_) < count_:
        count_ = limit - len(results_)
      default_params_ = {
          'count':
              str(count_),
          'filters':
              'List()',
          'origin':
              'GLOBAL_SEARCH_HEADER',
          'q':
              'all',
          'start':
              len(results_) + offset,
          'queryContext': ('List('
                           'spellCorrectionEnabled->true,'
                           'relatedSearchesEnabled->true,'
                           'kcardType->PROFILE|COMPANY'
                           ')')
      }
      default_params_.update(params)

      result_ = self._fetch(
          f'/search/blended?{urlencode(default_params_, safe="(),")}',
          headers={'accept': 'application/vnd.linkedin.normalized+json+2.1'})
      data_ = result_.json()

      new_elems = []
      elems_ = data_.get('data', {}).get('elements', [])
      for elem in elems_:
        new_elems.extend(elem.get('elements', {}))
      results_ = [*results_, *new_elems]

      # Breaks out the infinite loop if the maximum number of search results has
      # been reached, the maximum number of repeated requests has been exceeded,
      # or no new search results are returned.
      if ((-1 <= limit <= len(results_)) or len(results_) / count_ >=
          LinkedIn._MAX_REPEATED_REQUEST) or len(new_elems) == 0:
        break
    return results_

  def search_people(self, *, keywords: str = None, **kwargs) -> list[dict]:
    """Search for people on LinkedIn and return a list of results.
    
    Also, filters the search results by the given filter queries in `kwargs`
    and applies them to the `filters` parameter for the search function.
    
    Args:
      keywords: Keywords to search for.
    """
    filters_ = ['resultType->PEOPLE']

    def add_to_filter(key: str, to: str, /, *, value_type: type) -> None:
      """Adds the given key-mapped value to the non-local `filters_` list from
      the non-local `kwargs`.
      
      Args:
        key:        Key to which the filter value is mapped.
        to:         Label for the url.
        value_type: Type of the value.
      """
      nonlocal kwargs, filters_
      if kwargs.get(key, None) is None:
        return
      if isinstance(value_type, str):
        filters_ = [*filters_, f'{to}->{kwargs.get(key)}']
      elif isinstance(value_type, list):
        filters_ = [*filters_, f"{to}->{'|'.join(kwargs.get(key))}"]

    add_to_filter('connection_of', 'connectionOf', value_type=str)
    add_to_filter('network_depths', 'network', value_type=list)
    add_to_filter('network_depth', 'network', value_type=str)
    add_to_filter('regions', 'geoUrn', value_type=list)
    add_to_filter('schools', 'schools', value_type=list)
    add_to_filter('industries', 'industry', value_type=list)
    add_to_filter('current_company', 'currentCompany', value_type=list)
    add_to_filter('profile_languages', 'profileLanguage', value_type=list)

    params_ = {'filters': f"List({','.join(filters_)})"}
    if keywords:
      params_['keywords'] = keywords

    search_limit_ = kwargs.get('limit', None)
    search_offset_ = kwargs.get('offset', None)
    data_ = self.search(
        params_,
        limit=search_limit_ if search_limit_ is not None else -1,
        offset=search_offset_ if search_offset_ is not None else 0)

    result_ = []
    for item in data_:
      # Do not include a private profile if `include_private_profiles` is set
      # to `False` or `publicIdentifier` is absent.
      if not kwargs.get('include_private_profiles',
                        None) and 'publicIdentifier' not in item:
        continue
      result_ = [
          *result_, {
              'urn_id': utils.get_id_from_urn(item.get('targetUrn')),
              'distance': item.get('memberDistance', {}).get('value'),
              'public_id': item.get('publicIdentifier'),
              'tracking_id': utils.get_id_from_urn(item.get('trackingUrn')),
              'jobtitle': item.get('headline', {}).get('text'),
              'location': item.get('subline', {}).get('text'),
              'name': item.get('title', {}).get('text')
          }
      ]
    return result_

  def get_profile(self, public_id: str = None, urn_id: str = None) -> dict:
    """This function fetches the complete profile details for a given LinkedIn
    member using either their public ID or their URN ID. The function returns a
    dictionary containing the profile information.

    Args:
      public_id: Profile public id.
      urn_id:    Profile urn id.
    """
    assert public_id is None and urn_id is None, (
        'Expected any one of public_id or urn_id')

    result_ = self._fetch(
        f'/identity/profiles/{public_id or urn_id}/profileView')

    data_ = result_.json()
    if data_ and 'status' in data_ and data_['status'] != 200:
      self._logger.info('Request failed: %s', data_['message'])
      return {}

    profile_ = data_['profile']
    if 'miniProfile' in profile_:
      if 'picture' in profile_['miniProfile']:
        profile_['displayPictureUrl'] = profile_['miniProfile']['picture'][
            'com.linkedin.common.VectorImage']['rootUrl']
        images_data_ = profile_['miniProfile']['picture'][
            'com.linkedin.common.VectorImage']['artifacts']
        for image in images_data_:
          width, height, url_seg = operator.itemgetter(
              'width', 'height', 'fileIdentifyingUrlPathSegment')(image)
          profile_[f'img_{width}_{height}'] = url_seg

      profile_['profile_id'] = utils.get_id_from_urn(
          profile_['miniProfile']['entityUrn'])
      profile_['profile_urn'] = profile_['miniProfile']['entityUrn']
      profile_['member_urn'] = profile_['miniProfile']['objectUrn']
      profile_['public_id'] = profile_['miniProfile']['publicIdentifier']

      del profile_['miniProfile']
    del profile_['defaultLocale']
    del profile_['supportedLocales']
    del profile_['versionTag']
    del profile_['showEducationOnProfileTopCard']

    return profile_

  def add_connection(self,
                     profile_pub_id: str,
                     *,
                     message: str = '',
                     profile_urn: str = None) -> bool:
    """Sends a request to LinkedIn to send a connection invitation to the
    profile with the given public ID or URN ID. If a message is provided, it is
    included in the invitation.

    Args:
      profile_pub_id: Public ID of the LinkedIn profile to send connection
                      invitation to.
      message:        Message to include in the connection invitation. Must be
                      300 characters or less.
      profile_urn:    URN ID of the LinkedIn profile to send connection
                      invitation to. If not provided, the function will get it
                      by making a call to get_profile function.

    Returns:
      `True` if the request was successful and the invitation was sent,
      `False` otherwise.
    """
    if len(message) > 300:
      self._logger.warning(
          'Message "%s" too long - trimming it down to 300 characters...',
          message)
      message = message[:300:]

    if not profile_urn:
      profile_urn_string = self.get_profile(
          public_id=profile_pub_id)['profile_urn']
      profile_urn = profile_urn_string.split(':')[-1]

    tracking_id_ = utils.generate_tracking_id()
    payload_ = {
        'trackingId': tracking_id_,
        'message': message,
        'invitations': [],
        'excludeInvitations': [],
        'invitee': {
            'com.linkedin.voyager.growth.invitation.InviteeProfile': {
                'profileId': profile_urn
            }
        }
    }
    result_ = self._post(
        '/growth/normInvitations',
        data=json.dumps(payload_),
        headers={'accept': 'application/vnd.linkedin.normalized+json+2.1'})

    return result_.status_code != 201

  def remove_connection(self, profile_pub_id: str) -> bool:
    """Removes a connection with a LinkedIn user specified by their public ID.
    
    Args:
      profile_pub_id: Public ID of the LinkedIn user to remove connection with.

    Returns:
      `True` if connection removal was unsuccessful, `False` otherwise.
    """
    result_ = self._post(
        f'/identity/profiles/{profile_pub_id}/profileActions?action=disconnect',
        headers={'accept': 'application/vnd.linkedin.normalized+json+2.1'},
    )
    return result_.status_code != 200

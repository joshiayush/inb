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

from typing import Callable

import sys
import json
import time
import random
import logging
import operator

from urllib.parse import urlencode
from requests import cookies

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
  time.sleep(random.randint(2, 5))


class LinkedIn(object):  # pylint: disable=missing-class-docstring

  MAX_SEARCH_COUNT = 49

  _MAX_REPEATED_REQUEST = 200

  def __init__(self,
               username: str,
               password: str,
               *,
               authenticate: bool = True,
               refresh_cookies: bool = False,
               debug: bool = False,
               proxies: dict = None,
               cookies_: cookies.RequestsCookieJar = None,
               cookies_dir: str = None) -> None:
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
             **kwargs):
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
    evade()
    if not base_request:
      url = self.client.VOYAGER_API_BASE_URL
    else:
      url = self.client.LINKEDIN_BASE_URL
    url = f'{url}{uri}'
    return self.client.session.post(url, **kwargs)

  def search(self, params: dict, limit: int = -1, offset: int = 0) -> list:
    count_ = LinkedIn.MAX_SEARCH_COUNT
    if limit is None:
      limit = -1

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

      if ((-1 <= limit <= len(results_)) or len(results_) / count_ >=
          LinkedIn._MAX_REPEATED_REQUEST) or len(new_elems) == 0:
        break
    return results_

  def search_people(self, *, keywords: str = None, **kwargs) -> list:
    filters_ = ['resultType->PEOPLE']
    if kwargs.get('connection_of', None):
      filters_ = [*filters_, f'connectionOf->{kwargs.get("connection_of")}']
    if kwargs.get('network_depths', None):
      filters_ = [
          *filters_, f'network->{"|".join(kwargs.get("network_depths"))}'
      ]
    elif kwargs.get('network_depth', None):
      filters_ = [*filters_, f'network->{kwargs.get("network_depth")}']
    if kwargs.get('regions', None):
      filters_ = [*filters_, f'geoUrn->{"|".join(kwargs.get("regions"))}']
    if kwargs.get('industries', None):
      filters_ = [*filters_, f'industry->{"|".join(kwargs.get("industries"))}']
    if kwargs.get('current_company', None):
      filters_ = [
          *filters_,
          f'currentCompany->{"|".join(kwargs.get("current_company"))}'
      ]
    if kwargs.get('profile_languages', None):
      filters_ = [
          *filters_,
          f'profileLanguage->{"|".join(kwargs.get("profile_languages"))}'
      ]
    if kwargs.get('schools', None):
      filters_ = [*filters_, f'schools->{"|".join(kwargs.get("schools"))}']

    params_ = {'filters': f'List({",".join(filters_)})'}
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
                     message: str = None,
                     profile_urn: str = None) -> bool:
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
    result_ = self._post(
        f'/identity/profiles/{profile_pub_id}/profileActions?action=disconnect',
        headers={'accept': 'application/vnd.linkedin.normalized+json+2.1'},
    )
    return result_.status_code != 200

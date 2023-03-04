# pylint: disable=missing-module-docstring

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

import os
import time
import pickle
import shutil
import tempfile

from requests import cookies

from api import (cookierepo, exceptions as linkedin_api_exceptions)


class TestCookieRepository:

  def setup_method(self):
    self.username = 'ayush854032@gmail.com'
    self.cookie_jar = cookies.RequestsCookieJar()
    self.cookie_jar['cookie1'] = 'value1'
    self.cookie_jar['cookie2'] = 'value2'

    self.tmp_dir = tempfile.mkdtemp()
    self.cookie_repo = cookierepo.CookieRepository(self.username,
                                                   self.cookie_jar,
                                                   self.tmp_dir)

  def teardown_method(self):
    shutil.rmtree(self.tmp_dir)

  def test_get_cookie_dir(self):
    assert self.cookie_repo.get_cookie_dir() == self.tmp_dir

  def test__get_cookies_jar_file_path(self):
    expected_path = os.path.join(self.tmp_dir, self.username)
    assert os.fspath(
        self.cookie_repo._get_cookies_jar_file_path()) == expected_path  # pylint: disable=protected-access

  def test_save(self):
    cookie_jar_file_path = self.cookie_repo._get_cookies_jar_file_path()  # pylint: disable=protected-access
    assert not os.path.exists(cookie_jar_file_path)
    self.cookie_repo.save()
    assert os.path.exists(cookie_jar_file_path)

    with open(cookie_jar_file_path, 'rb') as jar_file:
      loaded_cookie_jar = pickle.load(jar_file)
    assert loaded_cookie_jar == self.cookie_jar

  def test_get_cookies(self):
    cookie_jar_file_path = self.cookie_repo._get_cookies_jar_file_path()  # pylint: disable=protected-access
    with open(cookie_jar_file_path, 'wb') as jar_file:
      pickle.dump(self.cookie_jar, jar_file)

    loaded_cookie_jar = self.cookie_repo.get_cookies()
    assert loaded_cookie_jar == self.cookie_jar

    # check expiration
    self.cookie_jar['JSESSIONID'] = '123456'
    expired_cookie = cookies.RequestsCookieJar()
    expired_cookie.set_cookie(
        cookies.create_cookie(name='JSESSIONID',
                              value='9068257311',
                              expires=time.time() + 60))
    self.cookie_jar.update(expired_cookie)
    with open(cookie_jar_file_path, 'wb') as jar_file:
      pickle.dump(self.cookie_jar, jar_file)
    try:
      self.cookie_repo.get_cookies()
      assert False, 'Expected exception not raised'
    except linkedin_api_exceptions.LinkedInSessionExpiredException:
      assert True

# pylint: disable=missing-module-docstring, protected-access

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
        self.cookie_repo._get_cookies_jar_file_path()) == expected_path

  def test_save(self):
    cookie_jar_file_path = self.cookie_repo._get_cookies_jar_file_path()
    assert not os.path.exists(cookie_jar_file_path)
    self.cookie_repo.save()
    assert os.path.exists(cookie_jar_file_path)

    with open(cookie_jar_file_path, 'rb') as jar_file:
      loaded_cookie_jar = pickle.load(jar_file)
    assert loaded_cookie_jar == self.cookie_jar

  def test_get_cookies(self):
    cookie_jar_file_path = self.cookie_repo._get_cookies_jar_file_path()
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

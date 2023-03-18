# pylint: disable=missing-module-docstring

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

from api import settings


def test_user_home_dir():
  assert settings.USER_HOME_DIR.is_dir()


def test_inb_user_dir():
  assert settings.INB_USER_DIR.is_dir()
  assert str(settings.INB_USER_DIR).startswith(str(settings.USER_HOME_DIR))


def test_inb_cookie_dir():
  assert settings.INB_COOKIE_DIR.is_dir()
  assert str(settings.INB_COOKIE_DIR).startswith(str(settings.INB_USER_DIR))
  assert str(settings.INB_COOKIE_DIR).endswith('/cookies')


def test_inb_log_dir():
  assert settings.INB_LOG_DIR.is_dir()
  assert str(settings.INB_LOG_DIR).startswith(str(settings.USER_HOME_DIR))
  assert str(settings.INB_LOG_DIR).endswith('/.inb/logs')


def test_logging_to_stream_enabled():
  assert not settings.LOGGING_TO_STREAM_ENABLED


def test_log_format_str():
  assert 'asctime' in settings.LOG_FORMAT_STR
  assert 'name' in settings.LOG_FORMAT_STR
  assert 'levelname' in settings.LOG_FORMAT_STR
  assert 'funcName' in settings.LOG_FORMAT_STR
  assert 'message' in settings.LOG_FORMAT_STR

  assert settings.LOG_FORMAT_STR.startswith('%(asctime)s')
  assert settings.LOG_FORMAT_STR.endswith('%(message)s')


def test_inb_version():
  assert settings.INB_VERSION == '1.0.0'

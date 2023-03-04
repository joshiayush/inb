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

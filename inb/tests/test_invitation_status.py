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

import sys
import pytest

from unittest import mock

from api.invitation import status


@pytest.fixture()
def person():
  return status.Person(name='John Smith',
                       occupation='Software Engineer',
                       location='San Francisco, CA',
                       profileid='john-smith',
                       profileurl='https://www.linkedin.com/in/john-smith')


@pytest.fixture()
def invitation():
  return status.Invitation()


def test_person_properties(person):  # pylint: disable=redefined-outer-name
  assert person.name == 'John Smith'
  assert person.occupation == 'Software Engineer'
  assert person.location == 'San Francisco, CA'
  assert person.profileid == 'john-smith'
  assert person.profileurl == 'https://www.linkedin.com/in/john-smith'


def test_invitation_set_invitation_fields_success(invitation):  # pylint: disable=redefined-outer-name
  invitation.set_invitation_fields(
      name='John Smith',
      occupation='Software Engineer',
      location='San Francisco, CA',
      profileid='john-smith',
      profileurl='https://www.linkedin.com/in/john-smith',
      status='sent',
      elapsed_time=10.0)

  assert invitation._name == 'John Smith'  # pylint: disable=protected-access
  assert invitation._occupation == 'Software Engineer'  # pylint: disable=protected-access
  assert invitation._location == 'San Francisco, CA'  # pylint: disable=protected-access
  assert invitation._profileid == 'john-smith'  # pylint: disable=protected-access
  assert invitation._profileurl == 'https://www.linkedin.com/in/john-smith'  # pylint: disable=protected-access
  assert invitation._success_rate == 1  # pylint: disable=protected-access
  assert invitation._failure_rate == 0  # pylint: disable=protected-access
  assert invitation._status == '✔'  # pylint: disable=protected-access
  assert invitation._elapsed_time == '10.0s'  # pylint: disable=protected-access


def test_invitation_set_invitation_fields_failure(invitation):  # pylint: disable=redefined-outer-name
  invitation.set_invitation_fields(
      name='John Smith',
      occupation='Software Engineer',
      location='San Francisco, CA',
      profileid='john-smith',
      profileurl='https://www.linkedin.com/in/john-smith',
      status='failed',
      elapsed_time=10.0)

  assert invitation._name == 'John Smith'  # pylint: disable=protected-access
  assert invitation._occupation == 'Software Engineer'  # pylint: disable=protected-access
  assert invitation._location == 'San Francisco, CA'  # pylint: disable=protected-access
  assert invitation._profileid == 'john-smith'  # pylint: disable=protected-access
  assert invitation._profileurl == 'https://www.linkedin.com/in/john-smith'  # pylint: disable=protected-access
  assert invitation._success_rate == 0  # pylint: disable=protected-access
  assert invitation._failure_rate == 1  # pylint: disable=protected-access
  assert invitation._status == '✘'  # pylint: disable=protected-access
  assert invitation._elapsed_time == '10.0s'  # pylint: disable=protected-access


def test_invitation_send_status_to_console(invitation):  # pylint: disable=redefined-outer-name
  status._SUCCESS_RATE = 0  # pylint: disable=protected-access
  status._FAILURE_RATE = 0  # pylint: disable=protected-access

  invitation.set_invitation_fields(
      name='John Smith',
      occupation='Software Engineer',
      location='San Francisco, CA',
      profileid='john-smith',
      profileurl='https://www.linkedin.com/in/john-smith',
      status='sent',
      elapsed_time=10.0)

  expected_output = ('  ✔  John Smith\n'
                     '  Software Engineer\n'
                     '  San Francisco, CA\n'
                     '  Success: 1  Failure: 0  Elapsed time: 10.0s\n')

  with mock.patch('click.echo') as mk_click_echo:
    invitation._send_status_to_console()  # pylint: disable=protected-access
    mk_click_echo.assert_has_calls([
        mock.call('', sys.stdout, True, True),
        mock.call(expected_output, sys.stdout, True, True),
        mock.call('', sys.stdout, True, True)
    ])


@pytest.fixture
def mock_sleep():
  with mock.patch('time.sleep') as mk_sleep:
    mk_sleep.time.return_value = 100.0
    yield mk_sleep


def test_invitation_display_invitation_status_on_console(
    invitation, mock_sleep):  # pylint: disable=redefined-outer-name
  # Test invitation sent
  with mock.patch('click.echo') as mk_echo:
    status._SUCCESS_RATE = 0  # pylint: disable=protected-access
    status._FAILURE_RATE = 0  # pylint: disable=protected-access
    invitation.set_invitation_fields(  # pylint: disable=redefined-outer-name
        name='John Smith',
        occupation='Software Engineer',
        location='San Francisco',
        profileid='john-smit',
        profileurl='https://linkedin.com/john-smith',
        status='sent',
        elapsed_time=10.0)
    invitation._send_status_to_console()  # pylint: disable=protected-access
    expected_output = ('  ✔  John Smith\n'
                       '  Software Engineer\n'
                       '  San Francisco\n'
                       '  Success: 1  Failure: 0  Elapsed time: 10.0s\n')
    mk_echo.assert_has_calls([
        mock.call('', sys.stdout, True, True),
        mock.call(expected_output, sys.stdout, True, True),
        mock.call('', sys.stdout, True, True)
    ])
    mock_sleep.assert_called_with(status.Invitation._SLEEP_TIME_AFTER_LOGGING)  # pylint: disable=protected-access

  # Test invitation failed
  with mock.patch('click.echo') as mk_echo:
    status._SUCCESS_RATE = 0  # pylint: disable=protected-access
    status._FAILURE_RATE = 0  # pylint: disable=protected-access
    invitation.set_invitation_fields(  # pylint: disable=redefined-outer-name
        name='John Smith',
        occupation='Software Engineer',
        location='San Francisco',
        profileid='john-smit',
        profileurl='https://linkedin.com/john-smith',
        status='failed',
        elapsed_time=10.0)
    invitation._send_status_to_console()  # pylint: disable=protected-access
    expected_output = ('  ✘  John Smith\n'
                       '  Software Engineer\n'
                       '  San Francisco\n'
                       '  Success: 0  Failure: 1  Elapsed time: 10.0s\n')
    mk_echo.assert_has_calls([
        mock.call('', sys.stdout, True, True),
        mock.call(expected_output, sys.stdout, True, True),
        mock.call('', sys.stdout, True, True)
    ])
    mock_sleep.assert_called_with(status.Invitation._SLEEP_TIME_AFTER_LOGGING)  # pylint: disable=protected-access

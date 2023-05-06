# pylint: disable=missing-module-docstring, redefined-outer-name, protected-access

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


def test_person_properties(person):
  assert person.name == 'John Smith'
  assert person.occupation == 'Software Engineer'
  assert person.location == 'San Francisco, CA'
  assert person.profileid == 'john-smith'
  assert person.profileurl == 'https://www.linkedin.com/in/john-smith'

def test_invitation_set_invitation_fields_success(invitation):
  invitation.set_invitation_fields(
      name='John Smith',
      occupation='Software Engineer',
      location='San Francisco, CA',
      profileid='john-smith',
      profileurl='https://www.linkedin.com/in/john-smith',
      status='sent',
      elapsed_time=10.0)

  assert invitation._name == 'John Smith'
  assert invitation._occupation == 'Software Engineer'
  assert invitation._location == 'San Francisco, CA'
  assert invitation._profileid == 'john-smith'
  assert invitation._profileurl == 'https://www.linkedin.com/in/john-smith'
  assert invitation._success_rate == 1
  assert invitation._failure_rate == 0
  assert invitation._status == '✔'
  assert invitation._elapsed_time == '10.0s'


def test_invitation_set_invitation_fields_failure(invitation):
  invitation.set_invitation_fields(
      name='John Smith',
      occupation='Software Engineer',
      location='San Francisco, CA',
      profileid='john-smith',
      profileurl='https://www.linkedin.com/in/john-smith',
      status='failed',
      elapsed_time=10.0)

  assert invitation._name == 'John Smith'
  assert invitation._occupation == 'Software Engineer'
  assert invitation._location == 'San Francisco, CA'
  assert invitation._profileid == 'john-smith'
  assert invitation._profileurl == 'https://www.linkedin.com/in/john-smith'
  assert invitation._success_rate == 0
  assert invitation._failure_rate == 1
  assert invitation._status == '✘'
  assert invitation._elapsed_time == '10.0s'


def test_invitation_send_status_to_console(invitation):
  status._SUCCESS_RATE = 0
  status._FAILURE_RATE = 0

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
    invitation._send_status_to_console()
    mk_click_echo.assert_has_calls([
        mock.call('', sys.stdout, True, True),
        mock.call(expected_output, sys.stdout, True, True),
        mock.call('', sys.stdout, True, True)
    ])

def test_invitation_send_status_to_console_with_empty_values(invitation):
  status._SUCCESS_RATE = 0
  status._FAILURE_RATE = 0

  invitation.set_invitation_fields(
      name='John Smith',
      occupation=None,
      location=None,
      profileid='john-smith',
      profileurl='https://www.linkedin.com/in/john-smith',
      status='sent',
      elapsed_time=10.0)

  expected_output = ('  ✔  John Smith\n'
                      '  \n'
                      '  \n'
                      '  Success: 1  Failure: 0  Elapsed time: 10.0s\n')

  with mock.patch('click.echo') as mk_click_echo:
    invitation._send_status_to_console()
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
    invitation, mock_sleep):
  # Test invitation sent
  with mock.patch('click.echo') as mk_echo:
    status._SUCCESS_RATE = 0
    status._FAILURE_RATE = 0
    invitation.set_invitation_fields(
        name='John Smith',
        occupation='Software Engineer',
        location='San Francisco',
        profileid='john-smit',
        profileurl='https://linkedin.com/john-smith',
        status='sent',
        elapsed_time=10.0)
    invitation._send_status_to_console()
    expected_output = ('  ✔  John Smith\n'
                       '  Software Engineer\n'
                       '  San Francisco\n'
                       '  Success: 1  Failure: 0  Elapsed time: 10.0s\n')
    mk_echo.assert_has_calls([
        mock.call('', sys.stdout, True, True),
        mock.call(expected_output, sys.stdout, True, True),
        mock.call('', sys.stdout, True, True)
    ])
    mock_sleep.assert_called_with(status.Invitation._SLEEP_TIME_AFTER_LOGGING)

  # Test invitation failed
  with mock.patch('click.echo') as mk_echo:
    status._SUCCESS_RATE = 0
    status._FAILURE_RATE = 0
    invitation.set_invitation_fields(
        name='John Smith',
        occupation='Software Engineer',
        location='San Francisco',
        profileid='john-smit',
        profileurl='https://linkedin.com/john-smith',
        status='failed',
        elapsed_time=10.0)
    invitation._send_status_to_console()
    expected_output = ('  ✘  John Smith\n'
                       '  Software Engineer\n'
                       '  San Francisco\n'
                       '  Success: 0  Failure: 1  Elapsed time: 10.0s\n')
    mk_echo.assert_has_calls([
        mock.call('', sys.stdout, True, True),
        mock.call(expected_output, sys.stdout, True, True),
        mock.call('', sys.stdout, True, True)
    ])
    mock_sleep.assert_called_with(status.Invitation._SLEEP_TIME_AFTER_LOGGING)

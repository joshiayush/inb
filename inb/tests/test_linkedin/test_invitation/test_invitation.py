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

from __future__ import annotations

import unittest
import textwrap

from linkedin.invitation import status


class TestGlobalVarSuccessAndFailureRate(unittest.TestCase):  # pylint: disable=missing-class-docstring

  def setUp(self) -> None:
    self._invitation = status.Invitation()
    self._invitation_fields = {
        'name': None,
        'occupation': None,
        'location': None,
        'mutual_connections': None,
        'profileid': None,
        'profileurl': None,
        'status': None,
        'elapsed_time': None,
    }
    status._SUCCESS_RATE = 0  # pylint: disable=protected-access
    status._FAILURE_RATE = 0  # pylint: disable=protected-access

  def test_global_var_failure_rate(self) -> None:
    self._invitation_fields['status'] = 'failed'
    failed_invitations = 10
    for _ in range(failed_invitations):
      self._invitation.set_invitation_fields(**self._invitation_fields)
    self.assertEqual(status._SUCCESS_RATE, 0)  # pylint: disable=protected-access
    self.assertEqual(status._FAILURE_RATE, failed_invitations)  # pylint: disable=protected-access

  def test_global_var_success_rate(self) -> None:
    self._invitation_fields['status'] = 'sent'
    success_invitations = 10
    for _ in range(success_invitations):
      self._invitation.set_invitation_fields(**self._invitation_fields)
    self.assertEqual(status._SUCCESS_RATE, success_invitations)  # pylint: disable=protected-access
    self.assertEqual(status._FAILURE_RATE, 0)  # pylint: disable=protected-access

  def tearDown(self) -> None:
    self._invitation_fields['status'] = None


class TestProtectedReplaceTemplateVarWithTemplateValue(unittest.TestCase):  # pylint: disable=missing-class-docstring

  def test_with_send_message_template(self) -> None:
    replace_template_var_with = [
        ('{{status}}', status._SENT_STATUS_SYMBOL),  # pylint: disable=protected-access
        ('{{name}}', 'Mohika Negi'),
        ('{{occupation}}', 'Doctor'),
        ('{{mutual_connections}}', '3 mutual connections'),
        ('{{success}}', '3'),
        ('{{failure}}', '0'),
        ('{{elapsed_time}}', '0.933s')
    ]
    # pylint: disable=protected-access
    expected_parsed_template = (
        f'{status._SENT_STATUS_SYMBOL}  Mohika Negi\n'
        'Doctor\n'
        '3 mutual connections\n'
        'Success:  3  Failure: 0  Elapsed time: 0.933s\n')
    # pylint: enable=protected-access
    actual_parsed_template = textwrap.dedent(
        status.Invitation._replace_template_var_with_template_value(  # pylint: disable=protected-access, line-too-long
            status._SEND_INVITATION_STATUS_TEMPL, replace_template_var_with)  # pylint: disable=protected-access
    )
    self.assertEqual(actual_parsed_template, expected_parsed_template)

  def test_with_search_message_template(self) -> None:
    replace_template_var_with = [
        ('{{status}}', status._SENT_STATUS_SYMBOL),  # pylint: disable=protected-access
        ('{{name}}', 'Mohika Negi'),
        ('{{occupation}}', 'Doctor'),
        ('{{location}}', 'India'),
        ('{{mutual_connections}}', '3 mutual connections'),
        ('{{success}}', '3'),
        ('{{failure}}', '0'),
        ('{{elapsed_time}}', '0.933s')
    ]
    # pylint: disable=protected-access
    expected_parsed_template = (
        f'{status._SENT_STATUS_SYMBOL}  Mohika Negi\n'
        'Doctor\n'
        'India\n'
        '3 mutual connections\n'
        'Success:  3  Failure: 0  Elapsed time: 0.933s\n')
    # pylint: enable=protected-access
    actual_parsed_template = textwrap.dedent(
        status.Invitation._replace_template_var_with_template_value(  # pylint: disable=protected-access, line-too-long
            status._SEARCH_INVITATION_STATUS_TEMPL, replace_template_var_with)  # pylint: disable=protected-access
    )
    self.assertEqual(actual_parsed_template, expected_parsed_template)

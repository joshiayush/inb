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
"""Invitation module to send invitation status to console."""

from __future__ import annotations

import time
import click

from typing import Any, List

_SUCCESS_RATE = 0
_FAILURE_RATE = 0

_SENT_STATUS_SYMBOL = '✔'
_FAILED_STATUS_SYMBOL = '✘'

_SEND_INVITATION_STATUS_TEMPL = """  {{status}}  {{name}}
  {{occupation}}
  {{mutual_connections}}
  Success:  {{success}}  Failure: {{failure}}  Elapsed time: {{elapsed_time}}
"""

_SEARCH_INVITATION_STATUS_TEMPL = """  {{status}}  {{name}}
  {{occupation}}
  {{location}}
  {{mutual_connections}}
  Success:  {{success}}  Failure: {{failure}}  Elapsed time: {{elapsed_time}}
"""


class Invitation(object):
  """Invitation API offeres the following methods to send invitation status to
  console.
  """

  _SLEEP_TIME_AFTER_LOGGING = 0.18

  def set_invitation_fields(self, name: str, occupation: str, location: str,
                            mutual_connections: str, profileid: str,
                            profileurl: str, status: str,
                            elapsed_time: int) -> None:
    self._name = name
    self._occupation = occupation
    self._location = location
    self._mutual_connections = mutual_connections
    self._profileid = profileid
    self._profileurl = profileurl

    self._success_rate = 0
    self._failure_rate = 0

    if status == 'sent':
      self._status = _SENT_STATUS_SYMBOL
      global _SUCCESS_RATE
      _SUCCESS_RATE += 1
      self._success_rate = _SUCCESS_RATE
    elif status == 'failed':
      self._status = _FAILED_STATUS_SYMBOL
      global _FAILURE_RATE
      _FAILURE_RATE += 1
      self._failure_rate = _FAILURE_RATE

    try:
      self._elapsed_time = str(elapsed_time)[0:5] + 's'
    except IndexError:
      self._elapsed_time = elapsed_time

  @staticmethod
  def _replace_template_var_with_template_value(
      message_template: str, replace_template_var_with: List[tuple]) -> str:
    for replace_template_var_with_value_pair in replace_template_var_with:
      message_template = message_template.replace(
          *replace_template_var_with_value_pair)
    return message_template

  def _fill_send_message_template(self) -> str:
    replace_template_var_with = [('{{status}}', self._status),
                                 ('{{name}}', self._name),
                                 ('{{occupation}}', self._occupation),
                                 ('{{mutual_connections}}',
                                  self._mutual_connections),
                                 ('{{success}}', str(self._success_rate)),
                                 ('{{failure}}', str(self._failure_rate)),
                                 ('{{elapsed_time}}', str(self._elapsed_time))]
    return self._replace_template_var_with_template_value(
        _SEND_INVITATION_STATUS_TEMPL, replace_template_var_with)

  def _fill_search_message_template(self) -> str:
    replace_template_var_with = [('{{status}}', self._status),
                                 ('{{name}}', self._name),
                                 ('{{occupation}}', self._occupation),
                                 ('{{location}}', self._location),
                                 ('{{mutual_connections}}',
                                  self._mutual_connections),
                                 ('{{success}}', str(self._success_rate)),
                                 ('{{failure}}', str(self._failure_rate)),
                                 ('{{elapsed_time}}', str(self._elapsed_time))]
    return self._replace_template_var_with_template_value(
        _SEARCH_INVITATION_STATUS_TEMPL, replace_template_var_with)

  def _send_status_to_console(self, sleep: bool = True) -> None:
    click.echo('', None, True, True)
    click.echo(
        self._fill_send_message_template() if self._location is None else
        self._fill_search_message_template(), None, True, True)
    click.echo('', None, True, True)
    if sleep is True:
      time.sleep(self._SLEEP_TIME_AFTER_LOGGING)

  def display_invitation_status_on_console(
      self,
      person: Any,
      status: str,  # pylint: disable=redefined-outer-name
      start_time: int) -> None:
    self.set_invitation_fields(name=person.name,
                               occupation=person.occupation,
                               location=getattr(person, 'location', None),
                               mutual_connections=person.mutual_connections,
                               profileid=person.profileid,
                               profileurl=person.profileurl,
                               status=status,
                               elapsed_time=time.time() - start_time)
    self._send_status_to_console()

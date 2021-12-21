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

import time

SUCCESS_RATE = 0
FAILURE_RATE = 0

SENT_STATUS_SYMBOL = '✔'
FAILED_STATUS_SYMBOL = '✘'

SEND_INVITATION_STATUS_TEMPL = """  {{status}}  {{name}}
  {{occupation}}
  {{mutual_connections}}
  ID: {{profileid}}
  URL: {{profileurl}}
  Success:  {{success}}  Failure: {{failure}}  Elapsed time: {{elapsed_time}}
"""

SEARCH_INVITATION_STATUS_TEMPL = """  {{status}}  {{name}}  • {{degree}}
  {{occupation}}
  {{location}}
  {{summary}}
  {{mutual_connections}}
  ID: {{profileid}}
  URL: {{profileurl}}
  Success:  {{success}}  Failure: {{failure}}  Elapsed time: {{elapsed_time}}
"""


class Invitation(object):
  _SLEEP_TIME_AFTER_LOGGING = 0.18

  def set_invitation_fields(self, name: str, occupation: str, location: str,
                            summary: str, mutual_connections: str,
                            profileid: str, profileurl: str, status: str,
                            elapsed_time: int) -> None:
    self._name = name
    self._occupation = occupation
    self._location = location
    self._summary = summary
    self._mutual_connections = mutual_connections
    self._profileid = profileid
    self._profileurl = profileurl

    self._success_rate = 0
    self._failure_rate = 0

    if status == 'sent':
      self._status = SENT_STATUS_SYMBOL
      global SUCCESS_RATE
      SUCCESS_RATE += 1
      self._success_rate = SUCCESS_RATE
    elif status == 'failed':
      self._status = FAILED_STATUS_SYMBOL
      global FAILURE_RATE
      FAILURE_RATE += 1
      self._failure_rate = FAILURE_RATE

    try:
      self._elapsed_time = str(elapsed_time)[0:5] + 's'
    except IndexError:
      self._elapsed_time = elapsed_time

  def _fill_send_message_template(self) -> str:
    message = SEND_INVITATION_STATUS_TEMPL
    message = message.replace('{{status}}', self._status)
    message = message.replace('{{name}}', self._name)
    message = message.replace('{{occupation}}', self._occupation)
    message = message.replace('{{mutual_connections}}',
                              self._mutual_connections)
    message = message.replace('{{profileid}}', self._profileid)
    message = message.replace('{{profileurl}}', self._profileurl)
    message = message.replace('{{success}}', str(self._success_rate))
    message = message.replace('{{failure}}', str(self._failure_rate))
    message = message.replace('{{elapsed_time}}', str(self._elapsed_time))
    return message

  def _fill_search_message_template(self) -> str:
    message = SEARCH_INVITATION_STATUS_TEMPL
    message = message.replace('{{status}}', self._status)
    message = message.replace('{{name}}', self._name)
    message = message.replace('{{occupation}}', self._occupation)
    message = message.replace('{{location}}', self._location)
    message = message.replace('{{summary}}', self._summary)
    message = message.replace('{{mutual_connections}}',
                              self._mutual_connections)
    message = message.replace('{{profileid}}', self._profileid)
    message = message.replace('{{profileurl}}', self._profileurl)
    message = message.replace('{{success}}', str(self._success_rate))
    message = message.replace('{{failure}}', str(self._failure_rate))
    message = message.replace('{{elapsed_time}}', str(self._elapsed_time))
    return message

  def status(self) -> None:
    if self._location is None and self._summary is None:
      message = self._fill_send_message_template()
    else:
      message = self._fill_search_message_template()

    print()
    print(message)
    print()

    time.sleep(self._SLEEP_TIME_AFTER_LOGGING)

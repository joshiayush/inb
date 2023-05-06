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

"""Invitation module to send invitation status to console."""

from __future__ import annotations

import sys
import time
import click

_SUCCESS_RATE = 0
_FAILURE_RATE = 0

_SENT_STATUS_SYMBOL = '✔'
_FAILED_STATUS_SYMBOL = '✘'

_SEARCH_INVITATION_STATUS_TEMPL = """  {{status}}  {{name}}
  {{occupation}}
  {{location}}
  Success: {{success}}  Failure: {{failure}}  Elapsed time: {{elapsed_time}}
"""


class Person:
  """A separate type for the LinkedIn user."""

  def __init__(
      self,
      *,
      name: str,
      occupation: str,
      location: str,
      profileid: str,
      profileurl: str,
  ):
    self.name = name
    self.occupation = occupation
    self.location = location
    self.profileid = profileid
    self.profileurl = profileurl


class Invitation(object):
  """Invitation API to set invitation status on console.
  
  Use function `display_invitation_status_on_console()` to print out
  invitation status on console for the given `Person` instance.
  """

  _SLEEP_TIME_AFTER_LOGGING = 0.18

  def set_invitation_fields(self, name: str, occupation: str, location: str,
                            profileid: str, profileurl: str, status: str,
                            elapsed_time: int) -> None:
    """Sets the invitation status fields from the given `Person` instance.
    
    Note, setting the success rate of the instance will not reflect in the
    actual success and failure counts for that you have to directly update
    the values of the global `_SUCCESS_RATE` and `_FAILURE_RATE` variables.

    Args:
      name:         Name of the person.
      occupation:   Occupation of the person.
      location:     Location of the person.
      profileid:    Profile ID of the person.
      profileurl:   Profile URL of the person.
      status:       Status of this invitation.
      elapsed_time: Time elapsed till now.
    """
    self._name = name
    self._occupation = occupation
    self._location = location
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

    # Try to trim the elapsed time to upto 4 digits.
    try:
      self._elapsed_time = str(elapsed_time)[0:5] + 's'
    except IndexError:
      self._elapsed_time = elapsed_time

  @staticmethod
  def _replace_template_var_with_template_value(
      message_template: str, replace_template_var_with: list[tuple]) -> str:
    """Replaces all the template variables in `_SEARCH_INVITATION_STATUS_TEMPL`
    with their actual values.
    
    Args:
      message_template:          The template message.
      replace_template_var_with: A list containing the replacement values for
                                  the template variables.
    """
    for replace_template_var_with_value_pair in replace_template_var_with:
      # fallback to when of the tuple items be None
      if replace_template_var_with_value_pair[1] is not None:
        message_template = message_template.replace(
            *replace_template_var_with_value_pair)
      else:
        # fill with an empty line
        message_template = message_template.replace(
            replace_template_var_with_value_pair[0], '')
    return message_template

  def _fill_search_message_template(self) -> str:
    """Fills the `_SEARCH_INVITATION_STATUS_TEMPL` with the properties inside
    `Person` instance.
    """
    replace_template_var_with = [('{{status}}', self._status),
                                 ('{{name}}', self._name),
                                 ('{{occupation}}', self._occupation),
                                 ('{{location}}', self._location),
                                 ('{{success}}', str(self._success_rate)),
                                 ('{{failure}}', str(self._failure_rate)),
                                 ('{{elapsed_time}}', str(self._elapsed_time))]
    return self._replace_template_var_with_template_value(
        _SEARCH_INVITATION_STATUS_TEMPL, replace_template_var_with)

  def _send_status_to_console(self, sleep: bool = True) -> None:
    """Private method to echo the invitation status on the console.
    
    This method fills the `_SEARCH_INVITATION_STATUS_TEMPL` with the given
    `Person` information and logs them off to the console using the `click`
    library which also takes care of the internationalization for us. Also,
    the library automatically detects the colors being used in the terminal
    and colorifies the given message accordingly.

    Args:
      sleep: Whether to sleep for `_SLEEP_TIME_AFTER_LOGGING` after logging.
    """
    click.echo('', sys.stdout, True, True)
    click.echo(self._fill_search_message_template(), sys.stdout, True, True)
    click.echo('', sys.stdout, True, True)
    if sleep is True:
      time.sleep(self._SLEEP_TIME_AFTER_LOGGING)

  def display_invitation_status_on_console(
      self,
      person: Person,
      status: str,  # pylint: disable=redefined-outer-name
      start_time: int) -> None:
    """Display the invitation status on the console for the given `Person`
    instance.

    The `set_invitation_fields()` method must be called before
    `_send_status_to_console()` method otherwise it will result in an error
    due to unknown definition of `self` attributes.

    Args:
      person:     Person instance with meta information.
      status:     Status of the current invitation.
      start_time: Clock in time of the invitation process.
    """
    self.set_invitation_fields(name=person.name,
                               occupation=person.occupation,
                               location=person.location,
                               profileid=person.profileid,
                               profileurl=person.profileurl,
                               status=status,
                               elapsed_time=time.time() - start_time)
    self._send_status_to_console()

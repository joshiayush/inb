# MIT License
#
# Copyright (c) 2019 Creative Commons
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!
from __future__ import annotations

import time

from typing import Any
from typing import Dict

from . import SUCCESS_RATE
from . import FAILURE_RATE
from . import SENT_STATUS_SYMBOL
from . import FAILED_STATUS_SYMBOL
from . import UNDEFINED_STATUS_SYMBOL


class Invitation(object):
  STATUS_NO: int = 0
  SLEEP_TIME_AFTER_LOGGING: int | float = 0.18

  def __init__(self: Invitation, **kwargs: Dict[Any, Any]) -> None:
    self.set_invitation_fields(**kwargs)

  def set_invitation_fields(self: Invitation,
                            name: str = '',
                            occupation: str = '',
                            status: str = '',
                            elapsed_time: int | float = 0) -> None:
    self._name = name
    if len(occupation) >= 50:
      self._occupation = occupation[0:50] + ' ' + '.'*3
    else:
      self._occupation = occupation
    self._success_rate = 0
    self._failure_rate = 0
    if status == "sent":
      self._status = SENT_STATUS_SYMBOL
      global SUCCESS_RATE
      SUCCESS_RATE += 1
      self._success_rate = SUCCESS_RATE
    elif status == "failed":
      self._status = FAILED_STATUS_SYMBOL
      global FAILURE_RATE
      FAILURE_RATE += 1
      self._failure_rate = FAILURE_RATE
    else:
      self._status = UNDEFINED_STATUS_SYMBOL
    try:
      self._elapsed_time = str(elapsed_time)[0:5] + "s"
    except IndexError:
      self._elapsed_time = elapsed_time

  def status(self: Invitation, come_back_by: int = 8) -> None:
    if Invitation.STATUS_NO > 0:
      print("\033[F" * come_back_by)
    else:
      Invitation.STATUS_NO += 1
    print()
    print(
        f"""{self._status} {self._name}\n\n"""
        f"""{self._occupation}\n\n"""
        f"""Success: {self._success_rate} Failed: {self._failure_rate} Elapsed: {self._elapsed_time}""")
    print()
    time.sleep(self.SLEEP_TIME_AFTER_LOGGING)

  def __del__(self: Invitation) -> None:
    Invitation.STATUS_NO = 0

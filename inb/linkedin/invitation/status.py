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

"""from __future__ imports must occur at the beginning of the file. DO NOT CHANGE!"""
from __future__ import annotations

import os
import time

from . import SUCCESS_RATE
from . import FAILURE_RATE
from . import SENT_STATUS_SYMBOL
from . import FAILED_STATUS_SYMBOL
from . import UNDEFINED_STATUS_SYMBOL

from console import RED_HEX
from console import CYAN_HEX
from console import GREEN_HEX
from console import YELLOW_HEX
from console import LIGHT_GREEN_HEX

from console.print import inbprint


class Invitation(object):

    SLEEP_TIME_AFTER_LOGGING: int | float = 0.18

    def __init__(
        self: Invitation,
        name: str,
        occupation: str,
        status: str = '',
        elapsed_time: int | float = 0
    ) -> None:
        self._name = name

        if len(occupation) >= 50:
            self._occupation = occupation[0:50] + ' ' + '.'*3
        else:
            self._occupation = occupation

        self._success_rate = 0
        self._failure_rate = 0

        if status == "sent":
            self._status = f"[bold {GREEN_HEX}]" + SENT_STATUS_SYMBOL

            global SUCCESS_RATE
            SUCCESS_RATE += 1
            self._success_rate = SUCCESS_RATE
        elif status == "failed":
            self._status = f"[bold {RED_HEX}]" + FAILED_STATUS_SYMBOL

            global FAILURE_RATE
            FAILURE_RATE += 1
            self._failure_rate = FAILURE_RATE
        else:
            self._status = f"[bold {CYAN_HEX}]" + UNDEFINED_STATUS_SYMBOL

        try:
            self._elapsed_time = str(elapsed_time)[0:5] + "s"
        except IndexError:
            self._elapsed_time = elapsed_time

    def __clear_screen(self: Invitation):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")

    def status(self: Invitation):
        self.__clear_screen()

        inbprint()
        inbprint(f"""{self._status} [bold {YELLOW_HEX}]{self._name}\n\n"""
                 f"""[bold {LIGHT_GREEN_HEX}]{self._occupation}\n\n"""
                 f"""[bold blink {GREEN_HEX}]Success: {self._success_rate} [bold blink {RED_HEX}]Failed: {self._failure_rate} [bold blink {CYAN_HEX}]Elapsed: {self._elapsed_time}""")
        inbprint()

        time.sleep(self.SLEEP_TIME_AFTER_LOGGING)

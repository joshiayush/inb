from __future__ import annotations

import os
import time

from . import SUCCESS_RATE
from . import FAILURE_RATE
from . import SENT_STATUS_SYMBOL
from . import FAILED_STATUS_SYMBOL
from . import UNDEFINED_STATUS_SYMBOL

from console.print import inbprint


class Invitation(object):

    def __init__(self: Invitation, name: str, occupation: str, status: str = '', elapsed_time: int = 0) -> None:
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

    def clears_creen(self: Invitation):
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")

    def status(self: Invitation):
        self.clears_creen()

        inbprint()
        inbprint(f"""{self._status} {self._name}\n\n"""
                 f"""{self._occupation}\n\n"""
                 f"""Success: {self._success_rate} Failed: {self._failure_rate} Elapsed: {self._elapsed_time}""")
        inbprint()

        time.sleep(0.18)

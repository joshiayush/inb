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

from typing import List

import platform
import subprocess


def ping(host: str = None) -> bool:
    """Returns True if host (str) responds to a ping request.

    Remember that a host may not respond to a ping (ICMP) request even if the host 
    name is valid.

    We avoid 'os.system' calls with 'subprocess.call' to avoid shell injection 
    vulnerability.

    :Args:
        - host: {str} Hostname.

    :Returns:
        - {bool} True if server responds, false otherwise.
    """
    if not host:
        host = "google.com"
    if platform.system().lower() == "windows":
        param = "-n"
    else:
        param = "-c"
    command: List[str] = ["ping", param, '1', host]
    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0

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

import re
import sys
import tty
import termios

from typing import TextIO


class Terminal(object):
    def setcursorposition(
        self: Terminal,
        x: int,
        y: int,
        file: TextIO = sys.stdout
    ) -> None:
        """Method setcursorposition() sets the console cursor position.

        :Args:
            - self: {Terminal}
            - x: {int} column number for the cursor
            - y: {int} row number for the cursor

        :Returns:
            - {None}
        """
        if file == None:
            file = sys.stdout
        file.write("%c[%d;%df" % (0x1B, y, x))

    def getcursorposition(self: Terminal) -> tuple:
        """Method getcursorposition() returns row and the column number at which the cursor is
        currently located.

        :Args:
            - self: {Terminal}

        :Returns:
            - {tuple} (row, column)
        """
        buffer: str = ''
        stdin: int = sys.stdin.fileno()
        tattr: list = termios.tcgetattr(stdin)

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()
            while True:
                buffer += sys.stdin.read(1)
                if buffer[-1] == 'R':
                    break
        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, tattr)

        # reading the actual values, but what if a keystroke appears while reading
        # from stdin? As dirty work around, getcursorposition() returns if this fails: None
        try:
            matches = re.match(r"^\x1b\[(\d*);(\d*)R", buffer)
            groups = matches.groups()
        except AttributeError:
            return None

        return (int(groups[0]), int(groups[1]))

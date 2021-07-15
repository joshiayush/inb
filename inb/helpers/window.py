from __future__ import annotations

import re
import sys
import tty
import termios

from console.print import inbprint


class Terminal(object):
    def setcursorposition(self: Terminal, x: int, y: int) -> None:
        """Method setcursorposition() sets the console cursor position.

        :Args:
            - self: {Terminal}
            - x: {int} column number for the cursor
            - y: {int} row number for the cursor

        :Returns:
            - {None}
        """
        inbprint("%c[%d;%df" % (0x1B, y, x), end='')

    def getcursorposition(self: Terminal) -> tuple:
        """Method getcursorposition() returns row and the column number at which the cursor is
        currently located.

        :Args:
            - self: {Terminal}

        :Returns:
            - {tuple} (row, column)
        """
        _buffer: str = ''
        _stdin: int = sys.stdin.fileno()
        _tattr: list = termios.tcgetattr(_stdin)

        try:
            tty.setcbreak(_stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()

            while True:
                _buffer += sys.stdin.read(1)

                if _buffer[-1] == "R":
                    break
        finally:
            termios.tcsetattr(_stdin, termios.TCSANOW, _tattr)

        # reading the actual values, but what if a keystroke appears while reading
        # from stdin? As dirty work around, getcursorposition() returns if this fails: None
        try:
            _matches = re.match(r"^\x1b\[(\d*);(\d*)R", _buffer)
            _groups = _matches.groups()
        except AttributeError:
            return None

        return (int(_groups[0]), int(_groups[1]))

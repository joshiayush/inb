import os

from console.print import printk


def gotoxy(x: int, y: int) -> None:
    """Function gotoxy() sets the console cursor position.

    :Args:
        - x: {int} column number for the cursor.
        - y: {int} row number for the cursor.

    :Returns:
        - {None}
    """
    printk("%c[%d;%df" % (0x1B, y, x), end='')

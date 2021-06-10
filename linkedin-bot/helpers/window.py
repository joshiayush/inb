import os

from console.print import printk


def terminal_size() -> list:
    """Function terminal_size() returns the very first size of the terminal window.

    :Args:
        - {None}

    :Returns:
        - {list} terminal size x and y.
    """
    return os.get_terminal_size()


def get_coords() -> list:
    """Function get_coords() returns the co-ordinates that are needed to set the Home 
    Logo near to the center according to the terminal size.

    :Args:
        - {None}

    :Returns:
        - {list} co-ordinates that sets the Logo near to the center.
    """
    if terminal_size()[0] >= 150:
        return [48, 5]

    if terminal_size()[0] >= 80:
        return [15, 2]

    return [15, 2]


def gotoxy(x: int, y: int) -> None:
    """Function gotoxy() sets the console cursor position.

    :Args:
        - x: {int} column number for the cursor.
        - y: {int} row number for the cursor.

    :Returns:
        - {None}
    """
    printk("%c[%d;%df" % (0x1B, y, x), end='')


def clear() -> None:
    """Function clear() clears the terminal screen.

    :Args:
        - {None}

    :Returns:
        - {None}
    """
    if os.name == "nt":
        os.system("cls")
        return

    if os.name == "posix":
        os.system("clear")
        return

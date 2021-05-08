import os

from helpers.print import printk


def terminal_size() -> list:
    """Function terminal_size() returns the size of the terminal when
    the LinkedIn Automator program executed, this functionality is required
    in order to set the Home Logo according to the terminal size. We declare
    this method static because we don't need to give this function an access
    to the object it's no use giving this function access to the object.

    return:
        terminal size.
    """
    return os.get_terminal_size()


def get_coords() -> list:
    """Function get_coords() returns the co-ordinates that are needed to set
    the Home Logo nearly to the center according to the terminal size. We
    declare this function static because we don't need to give this function
    an access to the object it's no use giving this function access to the object.

    return:
        co-ordinates that sets the Logo nearly to the center.
    """
    if terminal_size()[0] >= 150:
        return [48, 5]

    if terminal_size()[0] >= 80:
        return [15, 2]

    return [15, 2]


def gotoxy(x: int, y: int) -> None:
    """Function gotoxy() sets the console cursor position. We declare this
    function static because we don't need to give this function an access
    to the object it's no use giving this function access to the object.

    Args:
        x: column number for the cursor.
        y: row number for the cursor.
    """
    printk("%c[%d;%df" % (0x1B, y, x), end='')


def clear() -> None:
    """Method clear() clears the terminal screen for windows we use command
    `cls` and for linux based system we use command `clear`.
    """
    if os.name == "nt":
        os.system("cls")
        return

    if os.name == "posix":
        os.system("clear")
        return

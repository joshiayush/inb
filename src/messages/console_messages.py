from . import ConsoleMessages

from console.print import printk
from console.print import printRed
from console.print import printBlue
from console.print import printWhite
from console.print import printGreen
from console.print import printYellow


def send_to_console(_str: str = '', **kwargs: dict) -> None:
    if not ConsoleMessages.ENABLED:
        return

    if not kwargs:
        printk(_str)
        return

    if not "color" in kwargs:
        printk(_str, **kwargs)
        return

    if kwargs["color"] == 'w' or kwargs["color"] == "white":
        del kwargs["color"]
        printWhite(_str, **kwargs)
        return

    if kwargs["color"] == 'r' or kwargs["color"] == "red":
        del kwargs["color"]
        printRed(_str, **kwargs)
        return

    if kwargs["color"] == 'g' or kwargs["color"] == "green":
        del kwargs["color"]
        printGreen(_str, **kwargs)
        return

    if kwargs["color"] == 'b' or kwargs["color"] == "blue":
        del kwargs["color"]
        printBlue(_str, **kwargs)
        return

    if kwargs["color"] == 'y' or kwargs["color"] == "yellow":
        del kwargs["color"]
        printYellow(_str, **kwargs)
        return

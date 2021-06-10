import colorama  # type: ignore for Pylance you can remove it if you are not using Pylance

from . import Theme

from goto.goto import with_goto


"""No error squiggles when using Pylance. DO NOT REMOVE! if you are using Pylance."""
from typing import Any

goto: Any = ...
label: Any = ...


def printk(_str: str, **kwargs: dict) -> None:
    """Function printk() takes a string and displays that string on the terminal.
    This function also adds left 'whitespace' padding to the given string if there is a
    'pad' property present in the 'kwargs' otherwise it simply displays that string.

    :Args:
        - _str: {str} string to print on the screen.
        - kwargs: {dict} keyword arguments.

    :Returns:
        - {None}
    """
    if not kwargs:
        print(f"""{_str}""")
        return

    if not "pad" in kwargs:
        print(f"""{_str}""", **kwargs)
        return

    if "force" in kwargs:
        del kwargs["force"]

    if "start" in kwargs:
        print(end=kwargs["start"])
        del kwargs["start"]

    print(' '*int(kwargs["pad"]), end='')
    del kwargs["pad"]
    print(f"""{_str}""", **kwargs)


@with_goto
def printWhite(_str: str, **kwargs: dict) -> None:
    """Function printWhite() takes a string and displays that string in white color.

    :Args:
        - _str: {str} string to print on the terminal.
        - kwargs: {dict} keyword arguments.

    :Returns:
        - {None}
    """
    if not Theme.PARROT:
        if kwargs:
            if "force" in kwargs:
                if kwargs["force"] == "+f":
                    del kwargs["force"]
                    goto .begin

                del kwargs["force"]

            if "style" in kwargs:
                del kwargs["style"]

        printk(f"""{_str}""", **kwargs)
        return

    label .begin

    if not kwargs:
        printk(f"""{colorama.Fore.WHITE}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        printk(f"""{colorama.Fore.WHITE}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        printWhite(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        printWhite(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        printWhite(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return


@with_goto
def printRed(_str: str, **kwargs: dict) -> None:
    """Function printRed() takes a string and displays that string in red color.

    :Args:
        - _str: {str} string to print on the terminal.
        - kwargs: {dict} keyword arguments.

    :Returns:
        - {None}
    """
    if not Theme.PARROT:
        if kwargs:
            if "force" in kwargs:
                if kwargs["force"] == "+f":
                    del kwargs["force"]
                    goto .begin

                del kwargs["force"]

            if "style" in kwargs:
                del kwargs["style"]

        printk(f"""{_str}""", **kwargs)
        return

    label .begin

    if not kwargs:
        printk(f"""{colorama.Fore.RED}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        printk(f"""{colorama.Fore.RED}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        printRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        printRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        printRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return


@with_goto
def printGreen(_str: str, **kwargs: dict) -> None:
    """Function printGreen() takes a string and displays that string in green color.

    :Args:
        - _str: {str} string to print on the terminal.
        - kwargs: {dict} keyword arguments.

    :Returns:
        - {None}
    """
    if not Theme.PARROT:
        if kwargs:
            if "force" in kwargs:
                if kwargs["force"] == "+f":
                    del kwargs["force"]
                    goto .begin

                del kwargs["force"]

            if "style" in kwargs:
                del kwargs["style"]

        printk(f"""{_str}""", **kwargs)
        return

    label .begin

    if not kwargs:
        printk(f"""{colorama.Fore.GREEN}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        printk(f"""{colorama.Fore.GREEN}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        printGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        printGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        printGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return


@with_goto
def printBlue(_str: str, **kwargs: dict) -> None:
    """Function printBlue() takes a string and displays that string in blue color.

    :Args:
        - _str: {str} string to print on the terminal.
        - kwargs: {dict} keyword arguments.

    :Returns:
        - {None}
    """
    if not Theme.PARROT:
        if kwargs:
            if "force" in kwargs:
                if kwargs["force"] == "+f":
                    del kwargs["force"]
                    goto .begin

                del kwargs["force"]

            if "style" in kwargs:
                del kwargs["style"]

        printk(f"""{_str}""", **kwargs)
        return

    label .begin

    if not kwargs:
        printk(f"""{colorama.Fore.BLUE}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        printk(f"""{colorama.Fore.BLUE}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        printBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        printBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        printBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return


@with_goto
def printYellow(_str: str, **kwargs: dict) -> None:
    """Function printYellow() takes a string and displays that string in yellow color.

    :Args:
        - _str: {str} string to print on the terminal.
        - kwargs: {dict} keyword arguments.

    :Returns:
        - {None}
    """
    if not Theme.PARROT:
        if kwargs:
            if "force" in kwargs:
                if kwargs["force"] == "+f":
                    del kwargs["force"]
                    goto .begin

                del kwargs["force"]

            if "style" in kwargs:
                del kwargs["style"]

        printk(f"""{_str}""", **kwargs)
        return

    label .begin

    if not kwargs:
        printk(f"""{colorama.Fore.YELLOW}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        printk(f"""{colorama.Fore.YELLOW}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        printYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        printYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        printYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return

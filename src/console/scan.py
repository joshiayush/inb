import colorama  # type: ignore for Pylance you can remove it if you are not using Pylance

# importing `readline` this we need to import becuase when
# we take input from the terminal window and we press arrow
# keys then the characters that corresponds to the pressed
# key gets printed and we don't need that we need the cursor
# moving on pressing arrow keys.
import readline

from . import Theme

from python_goto.goto import with_goto

"""No error squiggles when using Pylance. DO NOT REMOVE! if you are using Pylance."""
from typing import Any

goto: Any = ...
label: Any = ...


def scank(_str: str, **kwargs: dict) -> str:
    """Function scank() is a dedicated input method for our LinkedIn `cli`
    (Command Line Interface), it also handles the Keyboard interrupt error.

    Args:
        - _str: string to display on the screen while taking user input.
        - kwargs: keyword arguments.

    return:
        returns the entered value.
    """
    _pad = 0

    if "start" in kwargs:
        print(end=kwargs["start"])
        del kwargs["start"]

    if "pad" in kwargs:
        _pad = kwargs["pad"]
        del kwargs["pad"]

    if not "end" in kwargs:
        return input(f"""{' '*int(_pad)}{_str}""")

    return input(f"""{' '*int(_pad)}{_str}{kwargs["end"]}""")


@with_goto
def scanWhite(_str: str, **kwargs: dict) -> str:
    """Function scanWhite() takes user input in white color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scank method takes besides string.

    return:
        returns the entered value.
    """
    if not Theme.PARROT:
        if kwargs and "force" in kwargs:
            if kwargs["force"] == "+f":
                del kwargs["force"]
                goto .begin

            del kwargs["force"]

        if kwargs and "style" in kwargs:
            del kwargs["style"]

        return scank(f"""{_str}""", **kwargs)

    label .begin

    if not kwargs:
        print(f"""{colorama.Fore.WHITE}""", end='')
        _inp = scank(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if "force" in kwargs:
        del kwargs["force"]

    if not "style" in kwargs:
        print(f"""{colorama.Fore.WHITE}""", end='')
        _inp = scank(f"""{_str}""", **kwargs)
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        _inp = scanWhite(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        _inp = scanWhite(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        _inp = scanWhite(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp


@with_goto
def scanRed(_str: str, **kwargs: dict) -> str:
    """Function scanRed() takes user input in red color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scank method takes besides string.

    return:
        returns entered value.
    """
    if not Theme.PARROT:
        if kwargs and "force" in kwargs:
            if kwargs["force"] == "+f":
                del kwargs["force"]
                goto .begin

            del kwargs["force"]

        if kwargs and "style" in kwargs:
            del kwargs["style"]

        return scank(f"""{_str}""", **kwargs)

    label .begin

    if not kwargs:
        print(f"""{colorama.Fore.RED}""", end='')
        _inp = scank(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if "force" in kwargs["force"]:
        del kwargs["force"]

    if not "style" in kwargs:
        print(f"""{colorama.Fore.RED}""", end='')
        _inp = scank(f"""{_str}""", **kwargs)
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        _inp = scanRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        _inp = scanRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        _inp = scanRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp


@with_goto
def scanGreen(_str: str, **kwargs: dict) -> str:
    """Function scanGreen() takes user input in green color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scank method takes besides string.

    return:
        returns entered value.
    """
    if not Theme.PARROT:
        if kwargs and "force" in kwargs:
            if kwargs["force"] == "+f":
                del kwargs["force"]
                goto .begin

            del kwargs["force"]

        if kwargs and "style" in kwargs:
            del kwargs["style"]

        return scank(f"""{_str}""", **kwargs)

    label .begin

    if not kwargs:
        print(f"""{colorama.Fore.GREEN}""", end='')
        _inp = scank(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if "force" in kwargs:
        del kwargs["force"]

    if not "style" in kwargs:
        print(f"""{colorama.Fore.GREEN}""", end='')
        _inp = scank(f"""{_str}""", **kwargs)
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        _inp = scanGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        _inp = scanGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        _inp = scanGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp


@with_goto
def scanBlue(_str: str, **kwargs: dict) -> str:
    """Function scanBlue() takes user input in blue color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scank method takes besides string.

    return:
        returns entered value.
    """
    if not Theme.PARROT:
        if kwargs and "force" in kwargs:
            if kwargs["force"] == "+f":
                del kwargs["force"]
                goto .begin

            del kwargs["force"]

        if kwargs and "style" in kwargs:
            del kwargs["style"]

        return scank(f"""{_str}""", **kwargs)

    label .begin

    if not kwargs:
        print(f"""{colorama.Fore.BLUE}""", end='')
        _inp = scank(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if "force" in kwargs:
        del kwargs["force"]

    if not "style" in kwargs:
        print(f"""{colorama.Fore.BLUE}""", end='')
        _inp = scank(f"""{_str}""", **kwargs)
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        _inp = scanBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        _inp = scanBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        _inp = scanBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp


@with_goto
def scanYellow(_str: str, **kwargs: dict) -> str:
    """Function scanYellow() takes user input in yellow color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scank method takes besides string.

    return:
        returns entered value.
    """
    if not Theme.PARROT:
        if kwargs and "force" in kwargs:
            if kwargs["force"] == "+f":
                del kwargs["force"]
                goto .begin

            del kwargs["force"]

        if kwargs and "style" in kwargs:
            del kwargs["style"]

        return scank(f"""{_str}""", **kwargs)

    label .begin

    if not kwargs:
        print(f"""{colorama.Fore.YELLOW}""", end='')
        _inp = scank(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if "force" in kwargs:
        del kwargs["force"]

    if not "style" in kwargs:
        print(f"""{colorama.Fore.YELLOW}""", end='')
        _inp = scank(f"""{_str}""", **kwargs)
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if kwargs["style"].lower() == 'b' or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end='')
        _inp = scanYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'n' or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end='')
        _inp = scanYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

    if kwargs["style"].lower() == 'd' or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end='')
        _inp = scanYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end='')
        return _inp

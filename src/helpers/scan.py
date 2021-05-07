import sys
import colorama

# importing `readline` this we need to import becuase when
# we take input from the terminal window and we press arrow
# keys then the characters that corresponds to the pressed
# key gets printed and we don't need that we need the cursor
# moving on pressing arrow keys.
import readline

from .print import printGreen


def scanf(_str, **kwargs):
    """Function scanf() is a dedicated input method for our LinkedIn `cli`
    (Command Line Interface), it also handles the Keyboard interrupt error.

    Args:
        - _str: string to display on the screen while taking user input.
        - kwargs: keyword arguments.

    return:
        returns the entered value.
    """
    if "start" in kwargs:
        print(end=kwargs["start"])
        del kwargs["start"]

    if "pad" in kwargs:
        print(' '*int(kwargs["pad"]), end='')
        del kwargs["pad"]

    if not "end" in kwargs:
        try:
            return input(f"""{_str}""")
        except KeyboardInterrupt:
            printGreen(f"""Piece""", style='b', start='\n', pad='1')
            sys.exit()

    try:
        return input(f"""{_str}{kwargs["end"]}""")
    except KeyboardInterrupt:
        printGreen(f"""Piece""", style='b', start='\n', pad='1')
        sys.exit()


def scanWhite(_str, **kwargs):
    """Function scanWhite() takes user input in white color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scanf method takes besides string.

    return:
        returns the entered value.
    """
    if not kwargs:
        print(f"""{colorama.Fore.WHITE}""", end='')
        _inp = scanf(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if not "style" in kwargs:
        print(f"""{colorama.Fore.WHITE}""", end='')
        _inp = scanf(f"""{_str}""", **kwargs)
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


def scanRed(_str, **kwargs):
    """Function scanRed() takes user input in red color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scanf method takes besides string.

    return:
        returns entered value.
    """
    if not kwargs:
        print(f"""{colorama.Fore.RED}""", end='')
        _inp = scanf(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if not "style" in kwargs:
        print(f"""{colorama.Fore.RED}""", end='')
        _inp = scanf(f"""{_str}""", **kwargs)
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


def scanGreen(_str, **kwargs):
    """Function scanGreen() takes user input in green color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scanf method takes besides string.

    return:
        returns entered value.
    """
    if not kwargs:
        print(f"""{colorama.Fore.GREEN}""", end='')
        _inp = scanf(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if not "style" in kwargs:
        print(f"""{colorama.Fore.GREEN}""", end='')
        _inp = scanf(f"""{_str}""", **kwargs)
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


def scanBlue(_str, **kwargs):
    """Function scanBlue() takes user input in blue color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scanf method takes besides string.

    return:
        returns entered value.
    """
    if not kwargs:
        print(f"""{colorama.Fore.BLUE}""", end='')
        _inp = scanf(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if not "style" in kwargs:
        print(f"""{colorama.Fore.BLUE}""", end='')
        _inp = scanf(f"""{_str}""", **kwargs)
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


def scanYellow(_str, **kwargs):
    """Function scanYellow() takes user input in yellow color.

    Args:
        _str: it is the string that needs to be printed on the terminal while taking 
            user input.
        **kwargs: are the key-value pair that scanf method takes besides string.

    return:
        returns entered value.
    """
    if not kwargs:
        print(f"""{colorama.Fore.YELLOW}""", end='')
        _inp = scanf(f"""{_str}""")
        print(f"""{colorama.Fore.RESET}""", end='')
        return _inp

    if not "style" in kwargs:
        print(f"""{colorama.Fore.YELLOW}""", end='')
        _inp = scanf(f"""{_str}""", **kwargs)
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

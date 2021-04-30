import colorama


def _print(_str, **kwargs):
    """Function _print() takes a string and displays that string on the terminal.
    This function also adds left 'whitespace' padding to the given string if there is a
    'pad' property present in the 'kwargs' otherwise it simply displays that string.

    Args:
        string: it is the string that needs to be printed on the terminal.
        **kwargs: are the key-value pair that print method takes besides string.
    """
    if not kwargs:
        print(f"""{_str}""")
        return

    if not "pad" in kwargs:
        print(f"""{_str}""", **kwargs)
        return

    print(" "*int(kwargs["pad"]), end="")
    del kwargs["pad"]
    print(f"""{_str}""", **kwargs)


def printRed(_str, **kwargs):
    """Function printRed() takes a string and displays that string in red color.

    Args:
        string: it is the string that needs to be printed on the terminal.
        **kwargs: are the key-value pair that print method takes besides string.
    """
    if not kwargs:
        _print(f"""{colorama.Fore.RED}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        _print(f"""{colorama.Fore.RED}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == "b" or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end="")
        printRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "n" or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end="")
        printRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "d" or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end="")
        printRed(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return


def printGreen(_str, **kwargs):
    """Function printGreen() takes a string and displays that string in red green.

    Args:
        string: it is the string that needs to be printed on the terminal.
        **kwargs: are the key-value pair that print method takes besides string.
    """
    if not kwargs:
        _print(f"""{colorama.Fore.GREEN}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        _print(f"""{colorama.Fore.GREEN}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == "b" or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end="")
        printGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "n" or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end="")
        printGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "d" or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end="")
        printGreen(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return


def printBlue(_str, **kwargs):
    """Function printBlue() takes a string and displays that string in blue color.

    Args:
        string: it is the string that needs to be printed on the terminal.
        **kwargs: are the key-value pair that print method takes besides string.
    """
    if not kwargs:
        _print(f"""{colorama.Fore.BLUE}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        _print(f"""{colorama.Fore.BLUE}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == "b" or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end="")
        printBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "n" or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end="")
        printBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "d" or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end="")
        printBlue(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return


def printYellow(_str, **kwargs):
    """Function printYellow() takes a string and displays that string in yellow color.

    Args:
        string: it is the string that needs to be printed on the terminal.
        **kwargs: are the key-value pair that print method takes besides string.
    """
    if not kwargs:
        _print(f"""{colorama.Fore.YELLOW}{_str}{colorama.Fore.RESET}""")
        return

    if not "style" in kwargs:
        _print(f"""{colorama.Fore.YELLOW}{_str}{colorama.Fore.RESET}""", **kwargs)
        return

    if kwargs["style"].lower() == "b" or kwargs["style"].lower() == "bright":
        del kwargs["style"]
        print(f"""{colorama.Style.BRIGHT}""", end="")
        printYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "n" or kwargs["style"].lower() == "normal":
        del kwargs["style"]
        print(f"""{colorama.Style.NORMAL}""", end="")
        printYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

    if kwargs["style"].lower() == "d" or kwargs["style"].lower() == "dim":
        del kwargs["style"]
        print(f"""{colorama.Style.DIM}""", end="")
        printYellow(_str, **kwargs)
        print(f"""{colorama.Style.RESET_ALL}""", end="")
        return

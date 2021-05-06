import sys
import colorama
from .print import printk


def _input():
    """Function _input() is a dedicated input method for our LinkedIn `cli`
    (Command Line Interface), it also handles the Keyboard interrupt error.
    We declare this function static because we don't need to give this
    function an access to the object it's no use giving this function access
    to the object.

    return:
        returns the entered value
    """
    try:
        printk(f"""{colorama.Style.BRIGHT}""", end="")
        printk(f"""{colorama.Fore.GREEN}""", end="")

        inp = input(f"""\n LinkedIn/> """)

        printk(f"""{colorama.Fore.RESET}""", end="")
        printk(f"""{colorama.Style.RESET_ALL}""", end="")

        return inp
    except KeyboardInterrupt:
        printk(f"""{colorama.Style.BRIGHT}""", end="")
        printk(f"""{colorama.Fore.GREEN}""", end="")

        printk("")
        printk(f"""Piece""", pad="1")

        printk(f"""{colorama.Fore.RESET}""", end="")
        printk(f"""{colorama.Style.RESET_ALL}""", end="")

        sys.exit()

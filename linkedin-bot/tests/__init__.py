"""Module tests to test linkedin-bot."""
import colorama


passed = "✔"
failed = "✘"

__name__ = "tests"
__package__ = "tests"


def message(msg: str = '', color: str = '') -> str:
    if color.lower() == 'r' or color.lower() == "red":
        return f"""{colorama.Style.NORMAL}{colorama.Fore.RED}{msg}{colorama.Style.RESET_ALL}"""

    if color.lower() == 'b' or color.lower() == "blue":
        return f"""{colorama.Style.NORMAL}{colorama.Fore.BLUE}{msg}{colorama.Style.RESET_ALL}"""

    if color.lower() == 'g' or color.lower() == "green":
        return f"""{colorama.Style.NORMAL}{colorama.Fore.GREEN}{msg}{colorama.Style.RESET_ALL}"""

    return f"""{msg}"""

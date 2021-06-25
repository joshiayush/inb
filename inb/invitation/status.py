import sys
import time
import colorama

from . import __success_rate
from . import __failure_rate

from console.print import printk
from console.print import printRed
from console.print import printBlue
from console.print import printGreen
from console.print import printWhite


def get_status(status: str = '') -> str:
    """Function get_status() sets the value of 'status' (status) according to the invitation 
    status which turns out to be a green ✔ mark on status 'sent' and a red ✘ mark on status 
    'failed'.  

    :Args:
        - status: {str} status of the request sent or failed.

    :Returns:
        - {str} invitation status.
    """
    global __success_rate
    global __failure_rate

    _stat = ''

    if status == "sent":
        """_stat = ✔"""
        _stat = u"\u2714"
        _stat = f"""{colorama.Fore.GREEN}""" + \
            _stat + f"""{colorama.Fore.RESET}"""

        __success_rate += 1
        return _stat

    if status == "failed":
        """_stat = ✘"""
        _stat = u"\u2718"
        _stat = f"""{colorama.Fore.RED}""" + \
            _stat + f"""{colorama.Fore.RESET}"""

        __failure_rate += 1
        return _stat


def show(name: str, occupation: str, status: str = '', elapsed_time: int = 0) -> None:
    """Function show() shows the invitation status on the terminal window in a specific format
    which is,

        ✔/✘ {Status} Person Name {Normal Style}
        Person Occupation {Dim Style}

        Succes rate: # {Green} Failure rate: # {Red} Elapsed time: # {Blue}

    :Args:
        - name: person's name.
        - occupation: person's occupation.
        - status: invitation status.
        - elasped_time: elasped time.

    :Returns:
        - {None}
    """
    global __success_rate
    global __failure_rate

    try:
        elapsed_time = str(elapsed_time)[0:5] + "s"
    except IndexError:
        elapsed_time = elapsed_time

    if len(occupation) >= 50:
        occupation = occupation[0:50] + ' ' + '.'*3

    if __success_rate != 0 or __failure_rate != 0:
        sys.stdout.write("\033[F\033[F\033[F\033[F\033[F\033[F")

    _stat = get_status(status=status)

    printk(' ', start='\n', pad='80', end='\r')

    printk(f"""{_stat}""", pad='4', end='')
    printWhite(f"""{name}""", style='n', pad='2')

    printk(' ', pad='80', end='\r')

    printWhite(f"""{occupation}""", style='d', pad='6')

    printk(' ', start='\n', pad='80', end='\r')

    printGreen(
        f"""Success: {__success_rate}""", style='b', pad='4', end='')
    printRed(f"""Failed: {__failure_rate}""",
             style='b', pad='2', end='')
    printBlue(
        f"""Elapsed: {elapsed_time}""", style='b', pad='2')

    printk("")

    time.sleep(0.18)


def reset() -> None:
    """Function reset() resets the static variables to their original values.

    :Args:
        - {None}

    :Returns:
        - {None}
    """
    global __success_rate
    global __failure_rate

    __success_rate = 0
    __failure_rate = 0

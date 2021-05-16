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


def calculate_status(status: str = '') -> str:
    """Method calculate_status() sets the value of '_stat' (status) according to the invitation 
    status which turns out to be a green ✔ mark on status 'sent' and a red ✘ mark on status 'failed'.  

    Args:
        - status: status of the request sent or failed.

    return:
        - {String} invitation status.
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
    """Method show() shows the invitation status on the terminal window in a specific format
    which is,

            ✔/✘ {Status} Person Name {Normal Style}
            Person Occupation {Dim Style}

            Succes rate: # {Green} Failure rate: # {Red} Elapsed time: # {Blue}

    Args:
        - self: class object which has the property 'calculate_status' in it.
        - obj: from which the name and occupation to be pulled.
        - status: status of the request sent or failed.
        - elapsed_time: how much time did it take to calculate and print the invitation status
            for every person.
    """
    global __success_rate
    global __failure_rate

    try:
        elapsed_time = str(elapsed_time)[0:5] + "s"
    except IndexError:
        elapsed_time = elapsed_time

    if len(occupation) >= 50:
        occupation = occupation[0:50] + "."*3

    if __success_rate != 0 or __failure_rate != 0:
        sys.stdout.write("\033[F\033[F\033[F\033[F\033[F\033[F")

    _stat = calculate_status(status=status)

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
    """Function reset() resets the class static variables to their original values once the 
    user is done sending the invitations to LinkedIn users.
    """
    global __success_rate
    global __failure_rate

    __success_rate = 0
    __failure_rate = 0

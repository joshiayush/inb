import sys
import time

from .print import printk
from .print import printRed
from .print import printBlue
from .print import printGreen
from .print import printWhite


class InvitationStatus(object):
    SUCCESS_RATE = 0
    FAILURE_RATE = 0

    @staticmethod
    def calculate_status(status=None):
        """Method calculate_status() sets the value of '_stat' (status) according to the invitation 
        status which turns out to be a green ✔ mark on status 'sent' and a red ✘ mark on status 'failed'.  

        Args:
            - self: class object which has the property 'calculate_status' in it.
            - status: status of the request sent or failed.

        return:
            - {String} invitation status.
        """
        _stat = ''

        if status == "sent":
            """_stat = ✔"""
            _stat = u"\u2714"
            _stat = f"""{colorama.Fore.GREEN}""" + \
                _stat + f"""{colorama.Fore.RESET}"""

            InvitationStatus.SUCCESS_RATE += 1
            return _stat

        if status == "failed":
            """_stat = ✘"""
            _stat = u"\u2718"
            _stat = f"""{colorama.Fore.RED}""" + \
                _stat + f"""{colorama.Fore.RESET}"""

            InvitationStatus.FAILURE_RATE += 1
            return _stat

    def show(self, obj=None, status=None, elapsed_time=0):
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
        name = obj[0]
        occupation = obj[1]

        try:
            _elapsed_time = str(elapsed_time)[0:5] + "s"
        except IndexError:
            pass

        if len(occupation) >= 50:
            occupation = occupation[0:50] + "."*3

        _stat = InvitationStatus.calculate_status(status=status)

        if InvitationStatus.SUCCESS_RATE != 0 or InvitationStatus.FAILURE_RATE != 0:
            sys.stdout.write("\033[F\033[F\033[F\033[F\033[F\033[F")

        printk("")
        printk(" ", pad="80", end="\r")

        printk(f"""{_stat}""", pad="4", end="")
        printWhite(f"""{name}""", style="n", pad="2")

        printk(" ", pad="80", end="\r")

        printWhite(f"""{occupation}""", style="d", pad="6")

        printk("")
        printk(" ", pad="80", end="\r")

        printGreen(
            f"""Success: {InvitationStatus.SUCCESS_RATE}""", style="b", pad="4", end="")
        printRed(f"""Failed: {InvitationStatus.FAILURE_RATE}""",
                 style="b", pad="2", end="")
        printBlue(
            f"""Elapsed: {colorama.Fore.BLUE}{elapsed_time}{colorama.Fore.RESET}""", style="b", pad="2")

        printk("")

        time.sleep(0.18)

    @staticmethod
    def reset():
        """Function reset() resets the class static variables to their original values once the 
        user is done sending the invitations to LinkedIn users.
        """
        InvitationStatus.SUCCESS_RATE = 0
        InvitationStatus.FAILURE_RATE = 0

    def __del__(self):
        """Destructor resets the class static attributes."""
        InvitationStatus.reset()

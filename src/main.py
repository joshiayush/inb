from LinkedInConnections import (
    LinkedInConnectionsGuided,
    LinkedInConnectionsAuto
)
from LinkedInJobs import LinkedInJobs
import os
import readline


class Main(object):

    def __init__(self):
        self.home()

    def _input(self):
        return input(" LinkedIn/> ")

    def clear(self):
        # for windows
        if os.name == 'nt':
            _ = os.system('cls')

        # for mac and linux(here, os.name is 'posix')
        elif os.name == 'posix':
            _ = os.system('clear')

    def move(self, x, y):
        print("\033[%d;%dH" % (y, x))

    def gotoxy(self, x, y):
        print("%c[%d;%df" % (0x1B, y, x), end='')

    def terminal_size(self):
        return os.get_terminal_size()

    def home(self):
        self.clear()
        self.gotoxy(48, 5)
        print(r"\\                      \\  //                  \\  \\             ")
        self.gotoxy(48, 6)
        print(r"\\        ()            \\ //                   \\  \\             ")
        self.gotoxy(48, 7)
        print(r"\\        \\  \\\\\\\\  \\//    \\\\\\\\        \\  \\  \\\\\\\\\  ")
        self.gotoxy(48, 8)
        print(r"\\        \\  \\    \\  \\\\    \\ ===//  \\\\\\\\  \\  \\     \\  ")
        self.gotoxy(48, 9)
        print(r"\\        \\  \\    \\  \\ \\   \\        \\    \\  \\  \\     \\  ")
        self.gotoxy(48, 10)
        print(r"\\\\\\\\  \\  \\    \\  \\  \\  \\\\\\\\  \\\\\\\\  \\  \\     \\  ")
        print()
        print()
        try:
            char = self._input()
            print(char.split("&&"))
        except KeyboardInterrupt:
            print("\nPiece")

if __name__ == "__main__":
    Main()

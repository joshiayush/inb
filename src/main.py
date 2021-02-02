from LinkedInConnections import (
    LinkedInConnectionsGuided,
    LinkedInConnectionsAuto
)
from LinkedInJobs import LinkedInJobs
import os
import readline


class Main(object):

    def __init__(self):
        self.init_commands()
        self.init_vars()
        self.home()
        self.run()

    def init_vars(self):
        self.user_email = ""
        self.user_password = ""

    def init_commands(self):
        self.commands = {
            "exit": quit,
            "help": self._help,
            "showcredentials": self.show,
            "devdetails": self.dev_details
        }

    def _help(self):
        print(" command -> config.user.email")
        print(" saves the given user's name as a credential field")
        print(" usage -> config.user.email=example@gmail.com")
        print()
        print(" command -> config.user.password")
        print(" saves the user's password as a credential field")
        print(" usage -> config.user.password=jhas'][/.fd0q3';")
        print()
        print(" command -> showcredentials")
        print(" puts the entered credentials on the screen")
        print()
        print(" command -> linkedin")
        print(" activates the given linkedin process")
        print(" usage -> linkedin send")
        print(" flag [send] starts the process of sending invitation")
        print(
            " usage -> linkedin invitation-manager [show/withdraw] [--send/--recieve]")
        print(" flag [invitation-manager] handles the invitation manager tab")
        print(
            " flag [show] shows the given type of invitation that you have in your account like send or recieved")
        print(" flag [withdraw] withdraws all the pending invitations")
        print(" usage -> linkedin mynetwork sendmessage")
        print(" flag [mynetwork] is the connection tab")
        print(" flag [sendmessage] sends a formal greet message to connections")
        print()
        print(" command -> devdetails")
        print(" prints the developer details like media links, emails and LinkedIn")

    def show(self):
        print(" %s" % (
            self.user_email if self.user_email else "use config.user.email to add user email"))
        print(" %s" % (
            self.user_password if self.user_password else "use config.user.password to add user password"))

    def dev_details(self):
        print(" Name -> Ayush Joshi")
        print(" Email:")
        print(" -> ayush854032@gmail.com (primary)")
        print(" -> joshiayush.joshiayush@gmail.com")
        print(" GitHub -> https://github.com/JoshiAyush")
        print(" LinkedIn -> https://www.linkedin.com/in/ayush-joshi-3600a01b7/")

    def _input(self):
        try:
            inp = input("\n LinkedIn/> ")
            return inp
        except KeyboardInterrupt:
            print("\n Piece")
            quit()

    def clear(self):
        """
        Function clear() clears the terminal screen

        for windows we use command `cls` and for linux

        based system we use command `clear`
        """
        if os.name == 'nt':
            _ = os.system('cls')
        elif os.name == 'posix':
            _ = os.system('clear')

    def move(self, x, y):
        print("\033[%d;%dH" % (y, x))

    def gotoxy(self, x, y):
        print("%c[%d;%df" % (0x1B, y, x), end='')

    def terminal_size(self):
        return os.get_terminal_size()

    def get_horiz_coords(self):
        if self.terminal_size()[0] >= 150:
            return [48, 5]
        elif self.terminal_size()[0] >= 80:
            return [15, 2]
        else:
            return [15, 2]

    def home(self):
        self.clear()
        x, y = self.get_horiz_coords()
        self.gotoxy(x, y)
        print(r"\\                      \\  //                  \\  \\             ")
        self.gotoxy(x, y+1)
        print(r"\\        ()            \\ //                   \\  \\             ")
        self.gotoxy(x, y+2)
        print(r"\\        \\  \\\\\\\\  \\//    \\\\\\\\        \\  \\  \\\\\\\\\  ")
        self.gotoxy(x, y+3)
        print(r"\\        \\  \\    \\  \\\\    \\ ===//  \\\\\\\\  \\  \\     \\  ")
        self.gotoxy(x, y+4)
        print(r"\\        \\  \\    \\  \\ \\   \\        \\    \\  \\  \\     \\  ")
        self.gotoxy(x, y+5)
        print(r"\\\\\\\\  \\  \\    \\  \\  \\  \\\\\\\\  \\\\\\\\  \\  \\     \\  ")
        print("\n Type help for more information!", end="\n")

    def Error(self):
        if self.command:
            print(f" `{self.command}` is not recognized as an internal command")

    def handle_linkedin_commands(self):
        pass

    def handle_configs(self):
        if "email" in self.command:
            self.user_email = self.command[self.command.find("=")+1:]
        elif "password" in self.command:
            self.user_password = self.command[self.command.find("=")+1:]

    def run(self):
        while True:
            self.command = self._input()
            if "linkedin" in self.command:
                self.handle_linkedin_commands()
            elif "=" in self.command:
                self.handle_configs()
            elif "=" not in self.command:
                # get() method of dictionary data type returns
                # value of passed argument if it is present
                # in dictionary otherwise second argument will
                # be assigned as default value of passed argument
                self.commands.get(self.command, self.Error)()


if __name__ == "__main__":
    Main()

import LinkedIn
import LinkedInConnections
import LinkedInJobs
import os
import readline


class Main(object):

    def __init__(self):
        self.init_commands()
        self.init_vars()
        self.home()
        self.run()

    def init_vars(self):
        self.data = {
            "user_email": "",
            "user_password": "",
            "job_keywords": "",
            "job_location": "",
            "driver_path": "/Python/LinkedIn Automater/driver/chromedriver"
        }

    def init_commands(self):
        self.commands = {
            "exit": quit,
            "help": self._help,
            "show": self.show,
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
        print(" command -> config.job.keywords")
        print(" saves the job keywords")
        print(" usage -> config.job.keywords=Data Science")
        print()
        print(" command -> config.job.location")
        print(" saves the job location")
        print(" usage -> config.job.location=Sanfransisco")
        print()
        print(" command -> show")
        print(" puts the entered user details on the screen")
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
            self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"))
        print(" %s" % (
            self.data["user_password"] if self.data["user_password"] else "use config.user.password to add user password"))

        if self.data["job_keywords"] or self.data["job_location"]:
            print(" Job Keywords -> %s" %
                  (self.data["job_keywords"] if self.data["job_keywords"] else None))
            print(" Job Location -> %s" %
                  (self.data["job_location"] if self.data["job_location"] else None))

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
        ? Function clear() clears the terminal screen
        ? for windows we use command `cls` and for linux
        ? based system we use command `clear`
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

    def linkedin_command_usage(self):
        print()
        print(" Missing flags [send] [invitation-manager] [mynetwork]")
        print(" Usage:")
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

    def handle_linkedin_commands(self):
        if self.command.split(" ")[1] == "send":
            if self.data["user_email"] and self.data["user_password"]:
                LinkedInConnections.LinkedInConnectionsAuto(self.data)
            else:
                print(
                    " Need credentials first use config.user.email/password to add them")
        elif self.command.split(" ")[1] == "invitation-manager":
            pass
        elif self.command.split(" ")[1] == "mynetwork":
            pass
        else:
            print("'%s' is not a linkedin command" %
                  (self.command.split(" ")[1]))

    def handle_configs(self):
        if "user.email" in self.command:
            self.data["user_email"] = self.command[self.command.find(
                "=")+1:].strip()
        elif "user.password" in self.command:
            self.data["user_password"] = self.command[self.command.find(
                "=")+1:].strip()
        elif "job.keywords" in self.command:
            self.data["job_keywords"] = self.command[self.command.find(
                "=")+1:].strip()
        elif "job.location" in self.command:
            self.data["job_location"] = self.command[self.command.find(
                "=")+1:].strip()

    def run(self):
        while True:
            self.command = self._input()
            if self.command.split(" ")[0] == "linkedin" and len(self.command.split(" ")) > 1:
                self.handle_linkedin_commands()
            elif self.command == "linkedin":
                self.linkedin_command_usage()
            elif "=" in self.command:
                self.handle_configs()
            else:
                # get() method of dictionary data type returns
                # value of passed argument if it is present
                # in dictionary otherwise second argument will
                # be assigned as default value of passed argument
                self.commands.get(self.command, self.Error)()


if __name__ == "__main__":
    Main()

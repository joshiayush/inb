
# * importing LinkedIn
import LinkedIn
# * importing `LinkedInConnections`
import LinkedInConnections
# * importing `LinkedInJobs`
import LinkedInJobs
# * importing `OS`
import os
# * importing `readline` this we need to import becuase when
# * we take input from the terminal window and we press arrow
# * keys then the characters that corresponds to the pressed
# * key gets printed and we don't need that we need the cursor
# * moving on pressing arrow keys.
import readline
# * importing `getpass` to take user password
import getpass
# * importing `colorama`
import colorama


class Main(object):
    """
    Class Main is the main class that gets executed after the user

    hits the command `./run.sh` on the terminal screen, this class 

    gives the `cli` (Command Line Interface) to the user. We don't

    have `GUI` (Graphical User Interface) here because I don't have

    any deign Idea in my mind yet.  
    """
    THEME = "parrot"

    def __init__(self):
        """
        Method __init__() initialize the commands and required variables,

        it also prints the Logo on the screen.
        """
        self.init_commands()    # ? initialize commands

        self.init_vars()        # ? initialize variable

        self.home()             # ? prints the logo

        self.run()              # ? start taking input

    def init_vars(self):
        """
        Method init_vars() intialize the dictionary that holds

        the user's details like credentials and jobs search, etc.
        """
        self.data = {
            "user_email": "",
            "user_password": "",
            "job_keywords": "",
            "job_location": "",
            "driver_path": "/Python/LinkedIn Automater/driver/chromedriver",
            "headless": True
        }
        self.theme = "parrot"
        self.help_with = {
            "linkedin": Main.help_with_linkedin,
            "show": Main.help_with_show,
            "devdetails": Main.help_with_devdetails,
            "clear": Main.help_with_clear,
            "exit": Main.help_with_exit
        }

    @staticmethod
    def set_theme(_theme):
        if _theme == "--parrot":
            Main.THEME = "parrot"
        elif _theme == "--normal":
            Main.THEME = "normal"
        Main.home()

    def init_commands(self):
        """
        Method init_commands() initialize the commands that LinkedIn

        Automater provides for now we have following commands,

        ! Commands:
            * exit: exit from the program
            * help: prints the commands and their usage 
            * show: shows the entered details
            * devdetails: prints the developer details
            * linkedin: activates the automation process
            * clear: clears the screen
        """
        self.commands = {
            "exit": quit,
            "help": self._help,
            "show": self.show,
            "devdetails": self.dev_details,
            "linkedin": self.handle_linkedin_commands,
            "clear": self.home
        }

    @staticmethod
    def style(style):
        styles = {
            "bright": colorama.Style.BRIGHT,
            "dim": colorama.Style.DIM,
            "normal": colorama.Style.NORMAL,
            "reset": colorama.Style.RESET_ALL
        }

        return styles.get(style, colorama.Style.RESET_ALL)

    @staticmethod
    def colorFore(color):
        colors = {
            "red": colorama.Fore.RED,
            "green": colorama.Fore.GREEN,
            "blue": colorama.Fore.BLUE,
            "reset": colorama.Fore.RESET,
            "lightred": colorama.Fore.LIGHTRED_EX,
            "lightgreen": colorama.Fore.LIGHTGREEN_EX,
            "lightblue": colorama.Fore.LIGHTBLUE_EX
        }

        if Main.THEME == "parrot":
            return colors.get(color, colorama.Fore.RESET)
        elif Main.THEME == "normal":
            return colors.get(color, colorama.Fore.RESET) if color == "red" or color == "reset" else " \b"

    @staticmethod
    def help_with_linkedin():
        """
        Method help_with_linkedin() shows how you can use the linkedin

        command in case you missed the flags with the linkedin command or 

        mistakenly applied wrong flags with the linkedin command.
        """
        pass

    @staticmethod
    def help_with_show():
        pass

    @staticmethod
    def help_with_devdetails():
        pass

    @staticmethod
    def help_with_clear():
        pass

    @staticmethod
    def help_with_exit():
        pass

    def _help(self, _with=None):
        """
        Method _help() provides a manual to the user, this guide

        is contains every information that a user needs in order to

        start linkedin automation.
        """
        Main._print(f"""{Main.style("bright")}""")
        Main._print(f"""{Main.colorFore("green")}""")
        if _with == None:
            Main._print(
                f"""LinkedIn Bash, version 1.2.0(1)-release (xrh-cclnk)""")
            Main._print(
                f"""These commands are defined internally. Type 'help' to see this list.""")
            Main._print(
                f"""Type 'command' --help to know more about that command.""")
            Main._print(f"""""")
            Main._print(
                f"""A ([]) around a command means that the command is optional.""")
            Main._print(
                f"""A (^) next to command means that the command is the default command.""")
            Main._print(
                f"""A (<>) around a name means that the field is required.""")
            Main._print(f"""A (/) between commands means that you can write either of these but not all.""")
            Main._print(
                f"""A (*) next to a name means that the command is disabled.""")
            Main._print(f"""""")
            Main._print(
                f"""linkedin [send] [suggestions^] --auto^/--guided [--headless]""")
            Main._print(
                f"""linkedin [send] [search industry=example&&location=india+usa+...] --auto^/--guided [--headless]""")
            Main._print(
                f"""linkedin [invitation-manager*] [show*] --sent*/--recieved* [--headless]""")
            Main._print(
                f"""linkedin [invitation-manager*] [withdraw*] [all*^/over > <days>*] [--headless]""")
            Main._print(
                f"""linkedin [mynetwork*] [show*] [all*/page > 1^+2+3+...*] [--headless]""")
            Main._print(
                f"""linkedin [mynetwork*] [sendmessage*] [all*] [--greet*^] [--headless]""")
            Main._print(f"""""")
            Main._print(f"""show""")
            Main._print(f"""""")
            Main._print(f"""devdetails""")
            Main._print(f"""""")
            Main._print(f"""theme <--parrot^/--normal>""")
            Main._print(f"""""")
            Main._print(f"""clear""")
            Main._print(f"""""")
            Main._print(f"""exit""")
        else:
            pass
        Main._print(f"""{Main.colorFore("reset")}""")

    def show(self):
        """
        Method show() gets executed once the user hit the command

        `show` this basically prints the information that user had

        entered.
        """
        print(f""" {Main.colorFore("green")}{Main.style("bright")}%s""" % (
            self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"))
        print(f""" {Main.colorFore("green")}{Main.style("bright")}%s""" % (
            "*"*len(self.data["user_password"]) if self.data["user_password"] else "use config.user.password to add user password"))

        # ! we print the information about job keys once we have any of
        # ! these two field otherwise we don't show it
        if self.data["job_keywords"] or self.data["job_location"]:
            print(f""" {Main.colorFore("green")}{Main.style("bright")}Job Keywords -> %s""" %
                  (self.data["job_keywords"] if self.data["job_keywords"] else None))
            print(f""" {Main.colorFore("green")}{Main.style("bright")}Job Location -> %s""" %
                  (self.data["job_location"] if self.data["job_location"] else None))

        # ! ask the user if (s)he want to see the password if yes show
        # ! them if not don't show them
        try:
            ch = input(
                f""" {Main.colorFore("green")}{Main.style("bright")}Show password anyway? [y/N]: """) if self.data["user_password"] else "n"
            if ch.lower() == "y":
                print(f""" {Main.colorFore("green")}{Main.style("bright")}%s""" % (
                    self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"))
                print(f""" {Main.colorFore("green")}{Main.style("bright")}%s""" % (
                    self.data["user_password"] if self.data["user_password"] else "use config.user.password to add user password"))
        except KeyboardInterrupt:
            print(
                f"""\n {Main.colorFore("green")}{Main.style("bright")}Piece{Main.style("reset")}""")
            quit()

    def dev_details(self):
        """
        Method dev_details() gets executed once the user hits the 

        command `devdetails` it basically shows the user's network

        profiles and mail address.
        """
        print(
            f""" {Main.colorFore("green") + Main.style("bright")}Name -> Ayush Joshi""")

        print(f""" {Main.colorFore("green")}Email:""")

        print(f""" {Main.colorFore("green")}-> ayush854032@gmail.com (primary)""")

        print(f""" {Main.colorFore("green")}-> joshiayush.joshiayush@gmail.com""")

        print(
            f""" {Main.colorFore("green")}GitHub -> https://github.com/JoshiAyush""")

        print(
            f""" {Main.colorFore("green")}LinkedIn -> https://www.linkedin.com/in/ayush-joshi-3600a01b7/{Main.colorFore("reset")}""")

    def _input(self):
        """
        Method _input() is a dedicated input method for our LinkedIn

        `cli` (Command Line Interface), it also handles the Keyboard

        interrupt error.

        ! return:
            * returns the entered value
        """
        try:
            inp = input(
                f"""\n {Main.colorFore("green")}{Main.style("bright")}LinkedIn/> """)
            print(end=f"""{Main.style("reset")}""")
            return inp

        except KeyboardInterrupt:
            print(
                f"""\n {Main.colorFore("green")}{Main.style("bright")}Piece{Main.style("reset")}""")
            quit()              # ? exit program silently

    @staticmethod
    def _print(string, **kwargs):
        if kwargs:
            print(f""" {string}""", **kwargs)
        else:
            print(f""" {string}""")

    @staticmethod
    def clear():
        """
        Method clear() clears the terminal screen

        for windows we use command `cls` and for linux

        based system we use command `clear`
        """
        if os.name == 'nt':
            _ = os.system('cls')
        elif os.name == 'posix':
            _ = os.system('clear')

    @staticmethod
    def gotoxy(x, y):
        """
        Method gotoxy() sets the console cursor position.

        ! Args:
            * x: column number for the cursor
            * y: row number for the cursor
        """
        print("%c[%d;%df" % (0x1B, y, x), end='')

    @staticmethod
    def terminal_size():
        """
        Method terminal_size() returns the size of the terminal when 

        the LinkedIn Automator program executed, this functionality

        is required in order to set the Home Logo according to the

        terminal size.

        ! return:
            * terminal size
        """
        return os.get_terminal_size()

    @staticmethod
    def get_coords():
        """
        Method get_coords() returns the co-ordinates that are

        needed to set the Home Logo nearly to the center according

        to the terminal size.

        ! return:
            * co-ordinates that sets the Logo nearly to the center 
        """
        if Main.terminal_size()[0] >= 150:
            return [48, 5]                      # ? return [48, 5] if full size
        elif Main.terminal_size()[0] >= 80:
            return [15, 2]                      # ? return [15, 2] if half size
        else:
            # ? else return [15, 2] (predicted)
            return [15, 2]

    @staticmethod
    def home():
        """
        Method home() prints the home logo on the screen which makes 

        the application more professional.
        """
        Main.clear()                # ? clears the screen first

        x, y = Main.get_coords()    # ? get the co-ordinates
        print(Main.style("bright"))
        print(Main.colorFore("green"))
        Main.gotoxy(x, y)           # ? apply co-ordinates
        print(r"\\                      \\  //                  \\  \\             ")
        Main.gotoxy(x, y+1)         # ? apply co-ordinates
        print(r"\\        ()            \\ //                   \\  \\             ")
        Main.gotoxy(x, y+2)         # ? apply co-ordinates
        print(r"\\        \\  \\\\\\\\  \\//    \\\\\\\\        \\  \\  \\\\\\\\\  ")
        Main.gotoxy(x, y+3)         # ? apply co-ordinates
        print(r"\\        \\  \\    \\  \\\\    \\ ===//  \\\\\\\\  \\  \\     \\  ")
        Main.gotoxy(x, y+4)         # ? apply co-ordinates
        print(r"\\        \\  \\    \\  \\ \\   \\        \\    \\  \\  \\     \\  ")
        Main.gotoxy(x, y+5)         # ? apply co-ordinates
        print(r"\\\\\\\\  \\  \\    \\  \\  \\  \\\\\\\\  \\\\\\\\  \\  \\     \\  ")

        # ? show a tip to automation
        print("\n Type help for more information!", end="\n")
        print(Main.colorFore("reset"))

    def Error(self):
        """
        Method Error() gets called when the entered command is

        not recognized.
        """
        if self.command:
            print(
                f""" {Main.colorFore("red")}{Main.style("bright")}`{self.command}` is not recognized as an internal command{Main.colorFore("reset")}""")

    def handle_linkedin_commands(self):
        """
        Method handle_linkedin_commands() calls the main LinkedIn classes

        according to the commands given by the user, it checks the flags

        that are applied with the `linkedin` command and calls the LinkedIn

        classes accordingly.
        """
        if self.command.split(" ")[1] == "send":
            if self.data["user_email"] and self.data["user_password"]:
                LinkedInConnections.LinkedInConnectionsAuto(self.data)
            else:
                print(
                    f""" {Main.colorFore("green")}{Main.style("bright")}Need credentials first use config.user.email/password to add them{Main.colorFore("reset")}""")
        elif self.command.split(" ")[1] == "invitation-manager":
            pass
        elif self.command.split(" ")[1] == "mynetwork":
            pass
        else:
            print("'%s' is not a linkedin command" %
                  (self.command.split(" ")[1]))

    def handle_configs(self):
        """
        Method handle_configs() basically saves the user's configurations

        that are passed by hitting the command `config.user.email/password`

        or `config.job/keywords/location`.
        """
        if "config.user.email" in self.command:
            self.data["user_email"] = self.command[self.command.find(
                "=")+1:].strip()
        elif "config.user.password" == self.command:
            self.data["user_password"] = getpass.getpass(prompt=" Password: ")
        elif "config.job.keywords" in self.command:
            self.data["job_keywords"] = self.command[self.command.find(
                "=")+1:].strip()
        elif "config.job.location" in self.command:
            self.data["job_location"] = self.command[self.command.find(
                "=")+1:].strip()
        else:
            self.Error()

    def run(self):
        """
        Method run() runs a infinite loop and starts the `cli`

        (Command Line Interface) and it actually starts listening

        to the commands and then it takes action accordingly.
        """
        while True:
            # ? get the command
            self.command = self._input()

            # ? parse the command
            if self.command.split(" ")[0] == "linkedin" and len(self.command.split(" ")) > 1:
                # ? handle the linkedin commands
                self.handle_linkedin_commands()
            elif self.command == "linkedin":
                # ? show the linkedin command usage
                self.help_with_linkedin()
            elif " " in self.command and self.command.split(" ")[0].strip() == "theme" and len(self.command.split(" ")) == 2:
                Main.set_theme(self.command.split(" ")[1].strip())
            elif "=" in self.command or "config.user.password" in self.command:
                # ? handle the config command
                self.handle_configs()
            else:
                # ? get() method of dictionary data type returns
                # ? value of passed argument if it is present
                # ? in dictionary otherwise second argument will
                # ? be assigned as default value of passed argument
                self.commands.get(self.command, self.Error)()


# ! Execute program
if __name__ == "__main__":
    Main()

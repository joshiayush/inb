
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
# * importing `re` regex
import re


class Main(object):
    """
    Class Main is the main class that gets executed after the user

    hits the command `./run.sh` on the terminal screen, this class 

    gives the `cli` (Command Line Interface) to the user. We don't

    have `GUI` (Graphical User Interface) here because I don't have

    any deign Idea in my mind yet.  

    ! Class Variable:
        * THEME: is the theme for our cli (command line interface)
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
            "linkedin": self.handle_linkedin_commands,
            "show": self.handle_show_commands,
            "developer": self.handle_developer_commands,
            "theme": self.handle_theme_commands,
            "clear": self.handle_clear_commands,
            "help": self.handle_help_commands,
            "exit": quit,
        }

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

        self.help_with = {
            "linkedin": Main.help_with_linkedin,
            "show": Main.help_with_show,
            "developer": Main.help_with_developer,
            "theme": Main.help_with_theme,
            "clear": Main.help_with_clear,
            "exit": Main.help_with_exit
        }

        self.theme = "parrot"

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
    def gotoxy(x, y):
        """
        Method gotoxy() sets the console cursor position.

        ! Args:
            * x: column number for the cursor
            * y: row number for the cursor
        """
        print("%c[%d;%df" % (0x1B, y, x), end='')

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
            "reset": colorama.Fore.RESET
        }

        if Main.THEME == "parrot":
            return colors.get(color, colorama.Fore.RESET)
        elif Main.THEME == "normal":
            return colors.get(color, colorama.Fore.RESET) if color == "red" or color == "reset" else " \b"

    def clear(self):
        """
        Method clear() clears the terminal screen

        for windows we use command `cls` and for linux

        based system we use command `clear`
        """
        if os.name == 'nt':
            _ = os.system('cls')
        elif os.name == 'posix':
            _ = os.system('clear')

    def home(self):
        """
        Method home() prints the home logo on the screen which makes 

        the application more professional.
        """
        self.clear()                # ? clears the screen first

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

    @staticmethod
    def _input():
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
            Main._print(f"""""", end=f"""{Main.style("reset")}""")
            return inp

        except KeyboardInterrupt:
            Main._print(
                f"""\n {Main.colorFore("green")}{Main.style("bright")}Piece{Main.style("reset")}""")
            quit()              # ? exit program silently

    @staticmethod
    def _print(string, **kwargs):
        if kwargs:
            print(f""" {string}""", **kwargs)
        else:
            print(f""" {string}""")

    def set_theme(self, _theme):
        if _theme == "--parrot":
            Main.THEME = "parrot"
            self.home()
        elif _theme == "--normal":
            Main.THEME = "normal"
            self.home()
        else:
            Main._print(
                f"""'{_theme}' can't be recognized as a 'theme' command""")

    @staticmethod
    def help_with_linkedin():
        """
        Method help_with_linkedin() shows how you can use the linkedin

        command in case you missed the flags with the linkedin command or 

        mistakenly applied wrong flags with the linkedin command.
        """
        Main._print(f"""{Main.style("bright")}{Main.colorFore("green")}""")
        Main._print(
            f"""linkedin [send] [suggestions^] --auto/--guided [--headless]""")
        Main._print(f"""`linkedin` command handles the linkedin process.""")
        Main._print(
            f"""`send` flag sends invitations according to the path given to it.""")
        Main._print(
            f"""`suggestions` flag lets linkedin know that it must use""")
        Main._print(f"""'MyNetwork' tab as a target.""")
        Main._print(
            f"""`--auto/--guided` flag tells the linkedin to start process in auto(recommended) or guided mode.""")
        Main._print(
            f"""`--headless` flag tells the program to start automation without opening the browser.""")
        Main._print(f"""""")
        Main._print(
            f"""linkedin [send] [search industry=example&&location=india+usa+...] --auto^/--guided [--headless]""")
        Main._print(f"""`linkedin` command handles the linkedin process.""")
        Main._print(
            f"""`send` flag sends invitations according to the path given to it.""")
        Main._print(
            f"""`search industry=example&&location=india+usa+...` flag lets linkedin know that it must""")
        Main._print(
            f"""go and search for people associated to the given industry and living in the given location.""")
        Main._print(
            f"""`--auto/--guided` flag tells the linkedin to start process in auto(recommended) or guided mode.""")
        Main._print(
            f"""`--headless` flag tells the program to start automation without opening the browser.""")
        Main._print(f"""""")
        Main._print(
            f"""linkedin [invitation-manager*] [show*] --sent*/--recieved* [--headless]""")
        Main._print(f"""`linkedin` command handles the linkedin process.""")
        Main._print(
            f"""`invitation-manager` flag tells the linkedin to start performing operations on""")
        Main._print(f"""invitation manager tab.""")
        Main._print(
            f"""`show` flag show tells the linkedin to show the people my account want to connect with.""")
        Main._print(
            f"""`--sent/--recieved` flag tells the linkedin to fetch either sent invitations or recieved ones.""")
        Main._print(
            f"""`--headless` flag tells the program to start automation without opening the browser.""")
        Main._print(f"""""")
        Main._print(
            f"""linkedin [invitation-manager*] [withdraw*] [all*^/over > <days>*] [--headless]""")
        Main._print(f"""`linkedin` command handles the linkedin process.""")
        Main._print(
            f"""`invitation-manager` flag tells the linkedin to start performing operations on""")
        Main._print(
            f"""`withdraw` flag tell the linkedin that you want to activate invitation withdrawing process.""")
        Main._print(
            f"""`all/over > <days>` flag tell to either withdraw all the sent invitations or""")
        Main._print(
            f"""use the amount of days given to withdraw sent invitations accordingly.""")
        Main._print(
            f"""`--headless` flag tells the program to start automation without opening the browser.""")
        Main._print(f"""""")
        Main._print(
            f"""linkedin [mynetwork*] [show*] [all*/page > 1^+2+3+...*] [--headless]""")
        Main._print(f"""`linkedin` command handles the linkedin process.""")
        Main._print(
            f"""`mynetwork` flag tell the linkedin to start operating on MyNetworks.""")
        Main._print(
            f"""`all/page > 1+2+3+...` flag tells either show all connections or use the pages given.""")
        Main._print(
            f"""`--headless` flag tells the program to start automation without opening the browser.""")
        Main._print(f"""""")
        Main._print(
            f"""linkedin [mynetwork*] [sendmessage*] [all*] [--greet*^] [--headless]""")
        Main._print(f"""`linkedin` command handles the linkedin process.""")
        Main._print(
            f"""`mynetwork` flag tell the linkedin to start operating on MyNetworks.""")
        Main._print(
            f"""`sendmessage` flag tells the linkedin to send messages to connections.""")
        Main._print(
            f"""`all` flag tells the linkedin to use all connections.""")
        Main._print(
            f"""`--greet` flag tells the linkedin to send greet message.""")
        Main._print(
            f"""`--headless` flag tells the program to start automation without opening the browser.""")
        Main._print(f"""{Main.colorFore("reset")}""")

    @staticmethod
    def help_with_show():
        Main._print(f"""{Main.style("bright")}{Main.colorFore("green")}""")
        Main._print(f"""`show` shows all the details you have entered like:""")
        Main._print(f"""user.email""")
        Main._print(
            f"""user.password (asks first if you want to see it really or not)""")
        Main._print(f"""job.keywords""")
        Main._print(f"""job.location""")
        Main._print(f"""{Main.colorFore("reset")}""")

    @staticmethod
    def help_with_developer():
        Main._print(f"""{Main.style("bright")}{Main.colorFore("green")}""")
        Main._print(f"""`developer` shows the developer details like:""")
        Main._print(f"""his number, email, profiles ...""")
        Main._print(f"""{Main.colorFore("reset")}""")

    @staticmethod
    def help_with_theme():
        Main._print(f"""{Main.style("bright")}{Main.colorFore("green")}""")
        Main._print(
            f"""`theme --parrot/--normal` changes the cli (command line theme) according to the given theme value.""")
        Main._print(f"""{Main.colorFore("reset")}""")

    @staticmethod
    def help_with_clear():
        Main._print(f"""{Main.style("bright")}{Main.colorFore("green")}""")
        Main._print(f"""`clear` clears the screen""")
        Main._print(f"""{Main.colorFore("reset")}""")

    @staticmethod
    def help_with_exit():
        Main._print(f"""{Main.style("bright")}{Main.colorFore("green")}""")
        Main._print(
            f"""`exit` exits the program and also does flushing jobs.""")
        Main._print(f"""{Main.colorFore("")}""")

    @staticmethod
    def help_with_help():
        Main._print(f"""{Main.style("bright")}{Main.colorFore("green")}""")
        Main._print(
            f"""`help` prints a list of commands that the Linkedin Automater have.""")
        Main._print(f"""{Main.colorFore("reset")}""")

    def get_command_lenght(self):
        return len(self.command.split(" "))

    def get_command_at_index(self, index):
        return self.command.split(" ")[index]

    def handle_help_commands(self):
        """
        Method _help() provides a manual to the user, this guide

        is contains every information that a user needs in order to

        start linkedin automation.
        """
        if len(self.command.split(" ")) >= 3 and self.command.split(" ")[2] == "--help":
            Main.help_with_help()
            if len(self.command.split(" ")) > 3:
                self.command = (
                    "command " + self.command.split(" ")[3]).strip()
                self.Error()
        else:
            Main._print(f"""{Main.style("bright")}""")
            Main._print(f"""{Main.colorFore("green")}""")

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
            Main._print(
                f"""A (/) between commands means that you can write either of these but not all.""")
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
            Main._print(f"""developer""")
            Main._print(f"""""")
            Main._print(f"""theme <--parrot^/--normal>""")
            Main._print(f"""""")
            Main._print(f"""clear""")
            Main._print(f"""""")
            Main._print(f"""exit""")

            Main._print(f"""{Main.colorFore("reset")}""")

    @staticmethod
    def show_job_details(self):
        """
        Function show_job_details() prints the job details that the user entered

        we print the information about job keys once we have any of these two 

        field otherwise we don't show it.
        """
        if self.data["job_keywords"] or self.data["job_location"]:
            Main._print(f"""{Main.colorFore("green")}{Main.style("bright")}Job Keywords -> %s""" %
                        (self.data["job_keywords"] if self.data["job_keywords"] else None))
            Main._print(f"""{Main.colorFore("green")}{Main.style("bright")}Job Location -> %s""" %
                        (self.data["job_location"] if self.data["job_location"] else None))

    @staticmethod
    def ask_to_show_password(self):
        """
        Function ask_to_show_password() asks the user if (s)he want to see the 

        password if yes show them if not don't show them, this is for security

        purpose.
        """
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

    def handle_show_commands(self):
        """
        Method show() gets executed once the user hit the command

        `show` this basically prints the information that user had

        entered.
        """
        Main._print(f"""{Main.colorFore("green")}{Main.style("bright")}%s""" % (
            self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"))
        Main._print(f"""{Main.colorFore("green")}{Main.style("bright")}%s""" % (
            "*"*len(self.data["user_password"]) if self.data["user_password"] else "use config.user.password to add user password"))

        Main.show_job_details(self)

        Main.ask_to_show_password(self)

    def handle_developer_commands(self):
        """
        Method dev_details() gets executed once the user hits the 

        command `devdetails` it basically shows the user's network

        profiles and mail address.
        """
        Main._print(f"""{Main.style("bright")}""")
        Main._print(f"""{Main.colorFore("green")}""")

        Main._print(f"""Name     :  Ayush Joshi""")
        Main._print(f"""Email    :  ayush854032@gmail.com (primary)""")
        Main._print(f"""Email    :  joshiayush.joshiayush@gmail.com""")
        Main._print(f"""Mobile   :  +91 8941854032 (Only WhatsApp)""")
        Main._print(f"""GitHub   :  https://github.com/JoshiAyush""")
        Main._print(
            f"""LinkedIn :  https://www.linkedin.com/in/ayush-joshi-3600a01b7/{Main.colorFore("reset")}""")

        Main._print(f"""{Main.colorFore("reset")}""")

    def handle_theme_commands(self):
        if self.get_command_lenght() >= 3 and self.get_command_at_index(2) == "--help":
            Main.help_with_theme()
            if self.get_command_lenght() > 3:
                self.command = (
                    "command " + self.get_command_at_index(3)).strip()
                self.Error()
        elif self.get_command_lenght() >= 3 and (
                self.get_command_at_index(2) == "--parrot" or self.get_command_at_index(2) == "--normal"):
            self.set_theme(self.get_command_at_index(2).strip())
        else:
            Main.help_with_theme()

    def handle_clear_commands(self):
        self.home()

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

    def Error(self):
        """
        Method Error() gets called when the entered command is

        not recognized.
        """
        if self.command:
            print(
                f""" {Main.colorFore("red")}{Main.style("bright")}`{self.command[8:]}` is not recognized as an internal command{Main.colorFore("reset")}""")

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
        if "config.user.password" == self.get_command_at_index(1):
            self.data["user_password"] = getpass.getpass(prompt=" Password: ")
        elif re.compile(r"config.user.email=*").search(self.command):
            self.data["user_email"] = self.command[self.command.find(
                "=")+1:].strip()
        elif re.compile(r"config.job.keywords=*").search(self.command):
            self.data["job_keywords"] = self.command[self.command.find(
                "=")+1:].strip()
        elif re.compile(r"config.job.location=*").search(self.command):
            self.data["job_location"] = self.command[self.command.find(
                "=")+1:].strip()
        else:
            self.Error()

    def handle_commands(self):
        _config_regex_ = re.compile(
            r"config.user.email|config.user.password|config.job.keywords|config.job.location")
        if _config_regex_.search(self.command):
            self.handle_configs()
        else:
            # ? get() method of dictionary data type returns
            # ? value of passed argument if it is present
            # ? in dictionary otherwise second argument will
            # ? be assigned as default value of passed argument.
            self.commands.get(self.command.split(" ")[1], self.Error)()

    def run(self):
        """
        Method run() runs a infinite loop and starts the `cli`

        (Command Line Interface) and it actually starts listening

        to the commands and then it takes action accordingly.
        """
        while True:
            # ? get the command and add 'command ' in it this way we
            # ? can handle the commands situated at list indices.
            self.command = ("command " + self._input()).strip()

            self.handle_commands()


# ! Execute program
if __name__ == "__main__":
    Main().run()

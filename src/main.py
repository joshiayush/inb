
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
    Class Main is the main class that gets executed after the user hits the

    command `./run.sh` on the terminal screen, this class gives the `cli`

    (Command Line Interface) to the user. We don't have `GUI` (Graphical User

    Interface) here because I don't have any deign Idea in my mind yet.

    ! Class Variable:
        * THEME: is the theme for our cli (command line interface).
    """
    THEME = "parrot"

    def __init__(self):
        """
        Method __init__() initializes the commands and required variables,

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
            * linkedin   : activates the automation process
            * show       : shows the entered details
            * developer  : prints the developer details
            * theme      : sets the given theme
            * clear      : clears the screen
            * help       : prints the commands and their usage
            * exit       : exit from the program
        """
        self.commands = {
            "linkedin": self.handle_linkedin_commands,
            "show": self.handle_show_commands,
            "developer": self.handle_developer_commands,
            "theme": self.handle_theme_commands,
            "clear": self.handle_clear_commands,
            "help": self.handle_help_commands,
            "exit": self.handle_exit_commands,
        }

    def init_vars(self):
        """
        Method init_vars() intialize the dictionary that holds the user's

        details like credentials and jobs search, etc, it also initializes

        a dictionary which conatins commands and their corresponding help

        functions, there's one more variable that gets initializes that is

        the theme variable for our cli (Command Line Interface).
        """
        self.data = {
            "user_email": "",
            "user_password": "",
            "job_keywords": "",
            "job_location": "",
            "driver_path": "/Python/LinkedIn Automater/driver/chromedriver",
            "headless": False
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
    def terminal_size():
        """
        Function terminal_size() returns the size of the terminal when the LinkedIn

        Automator program executed, this functionality is required in order to set

        the Home Logo according to the terminal size. We declare this method static

        because we don't need to give this function an access to the object its no

        use giving this function access to the object.

        ! return:
            * terminal size.
        """
        return os.get_terminal_size()

    @staticmethod
    def get_coords():
        """
        Function get_coords() returns the co-ordinates that are needed to set the Home

        Logo nearly to the center according to the terminal size. We declare this function

        static because we don't need to give this function an access to the object its

        no use giving this function access to the object.

        ! return:
            * co-ordinates that sets the Logo nearly to the center.
        """
        if Main.terminal_size()[0] >= 150:
            return [48, 5]                      # ? return [48, 5] if full size
        elif Main.terminal_size()[0] >= 80:
            return [15, 2]                      # ? return [15, 2] if half size
        else:
            return [15, 2]      # ? else return [15, 2] (predicted)

    @staticmethod
    def gotoxy(x, y):
        """
        Function gotoxy() sets the console cursor position. We declare this function

        static because we don't need to give this function an access to the object

        its no use giving this function access to the object.

        ! Args:
            * x: column number for the cursor.
            * y: row number for the cursor.
        """
        print("%c[%d;%df" % (0x1B, y, x), end='')

    @staticmethod
    def style(style):
        """
        Function style() returns the text style that we are printing on the terminal,

        it uses 'colorama' module to generate unicode for the given style value. We

        declare this function static because we don't need to give this function an

        access to the object its no use giving this function access to the object.

        ! Args:
            * style: it is the style to be given to the text on the screen.

        ! return:
            * text style.
        """
        styles = {
            "bright": colorama.Style.BRIGHT,
            "dim": colorama.Style.DIM,
            "normal": colorama.Style.NORMAL,
            "reset": colorama.Style.RESET_ALL
        }

        return styles.get(style, colorama.Style.RESET_ALL)

    @staticmethod
    def colorFore(color):
        """
        Function colorFore() returns the text color according to the theme enabled,

        it returns the text color only if the theme is set to '--parrot' otherwise

        it only returns a unicode for color 'red' or 'reset' command if the theme is

        set to '--normal'. We declare this function static because we don't need to

        give this function an access to the object its no use giving this function

        access to the object.

        ! Args:
            * color: it is the color that we need to return the unicode for.

        ! return:
            * unicode for color.
        """
        colors = {
            "red": colorama.Fore.RED,
            "green": colorama.Fore.GREEN,
            "blue": colorama.Fore.BLUE,
            "reset": colorama.Fore.RESET
        }

        # ! checking if the theme is set to '--parrot'
        if Main.THEME == "parrot":
            return colors.get(color, colorama.Fore.RESET)
        # ! return normal style if theme is set to '--normal'
        elif Main.THEME == "normal":
            return colors.get(color, colorama.Fore.RESET) if color == "red" or color == "reset" else " \b"

    @staticmethod
    def match_string_with_colorama_objects(string):
        """
        Function match_string_with_colorama_objects() returns a boolean True value if

        the string matches with a colorama generated unicode otherwise it returns False.

        This functionality is needed to perfectly print strings on the terminal window

        because for print functionality I have created a class method which adds a space

        before every string given to it. We declare this function static because we don't

        need to give this function an access to the object its no use giving this function

        access to the object.

        ! Args:
            * string: it is the string that we need to match with the colorama generated
            * unicode

        ! return:
            * return a boolean value
        """
        if string == Main.style("bright") or string == Main.style("dim") or string == Main.style("normal") \
                or string == Main.style("reset"):
            return True
        elif string == Main.colorFore("red") or string == Main.colorFore("green") or string == Main.colorFore("blue") \
                or string == Main.colorFore("reset"):
            return True
        else:
            return False

    def clear(self):
        """
        Method clear() clears the terminal screen for windows we use command `cls` and

        for linux based system we use command `clear`.
        """
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')

    def home(self):
        """
        Method home() prints the home logo on the screen which makes the application look

        more sexy.
        """
        self.clear()                # ? clears the screen first

        x, y = Main.get_coords()    # ? get the co-ordinates

        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

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
        Main._print(f"""\n Type help for more information!""", end="\n")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def _input():
        """
        Function _input() is a dedicated input method for our LinkedIn `cli` (Command Line

        Interface), it also handles the Keyboard interrupt error. We declare this function

        static because we don't need to give this function an access to the object its no

        use giving this function access to the object.

        ! return:
            * returns the entered value
        """
        try:
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("green")}""", end="")

            inp = input(f"""\n LinkedIn/> """)

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")

            return inp

        except KeyboardInterrupt:
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("green")}""", end="")

            Main._print(f"""\n Piece""")

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")

            exit()              # ? exit program silently

    @staticmethod
    def _print(string, **kwargs):
        """
        Function _print() is a dedicated print() function for our cli (Command Line

        Interface) it basically adds a space to every value that needs to be printed

        on the terminal. We declare this function static because we don't need to give

        this function an access to the object its no use giving this function access to

        the object.

        ! Args:
            * string: it is the string that needs to be printed on the terminal.
            * **kwargs: are the key-value pair that print method takes besides string.
        """
        # ! don't add space to the print value if the print value is a colorama
        # ! generated unicode
        if Main.match_string_with_colorama_objects(string):
            if kwargs:
                print(f"""{string}""", end="")
            else:
                print(f"""{string}""")
        else:
            if kwargs:
                print(f""" {string}""", **kwargs)
            else:
                print(f""" {string}""")

    def set_theme(self, _theme):
        """
        Function set_theme() sets the cli (Command Line Interface) theme according

        to the value given.

        ! Args:
            * _theme: it is the theme that the we need to give to our cli after
            * user has entered it.
        """
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
    def help_with_configs():
        pass

    @staticmethod
    def help_with_linkedin():
        """
        Method help_with_linkedin() shows how you can use the linkedin command in case

        you missed the flags with the linkedin command or mistakenly applied wrong flags

        with the linkedin command. We declare this function static because we don't need

        to give this function an access to the object its no use giving this function

        access to the object.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

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
            f"""go and search for people associated to the given industry (use (%) for space between words in industry)""")
        Main._print(f"""and living in the given location.""")
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
            f"""linkedin [invitation-manager*] [ignore*/withdraw*] [all*^/over > <days>*] [--headless]""")
        Main._print(f"""`linkedin` command handles the linkedin process.""")
        Main._print(
            f"""`invitation-manager` flag tells the linkedin to start performing operations on""")
        Main._print(
            f"""`ignore/withdraw` flag tells the linkedin that you want to activate invitation ignoring or withdrawing process.""")
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

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def help_with_show():
        """
        Function help_with_show() shows you how you can use the 'show' command in case

        you entered wrong command. We declare this function static because we don't

        need to give this function an access to the object its no use giving this

        function access to the object.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(f"""`show` shows all the details you have entered like:""")
        Main._print(f"""user.email""")
        Main._print(
            f"""user.password (asks first if you want to see it really or not)""")
        Main._print(f"""job.keywords""")
        Main._print(f"""job.location""")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def help_with_developer():
        """
        Function help_with_developer() shows you how you can use the 'developer' command

        in case you entered wrong command. We declare this function static because we

        don't need to give this function an access to the object its no use giving this

        function access to the object.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(f"""`developer` shows the developer details like:""")
        Main._print(f"""his number, email, profiles ...""")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def help_with_theme():
        """
        Function help_with_theme() shows you how you can use the 'theme' command

        in case you entered wrong command or entered a un-matching flag. We declare

        this function static because we don't need to give this function an access

        to the object its no use giving this function access to the object.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(
            f"""`theme --parrot/--normal` changes the cli (command line theme) according to the given theme value.""")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def help_with_clear():
        """
        Function help_with_clear() shows you how you can use the 'clear' command

        in case you entered wrong command. We declare this function static because we

        don't need to give this function an access to the object its no use giving this

        function access to the object.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(f"""`clear` clears the screen""")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def help_with_exit():
        """
        Function help_with_exit() shows you how you can use the 'exit' command

        in case you entered wrong command. We declare this function static because we

        don't need to give this function an access to the object its no use giving this

        function access to the object.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(
            f"""`exit` exits the program and also does flushing jobs.""")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def help_with_help():
        """
        Function help_with_help() shows you how you can use the 'help' command

        in case you entered wrong command. We declare this function static because we

        don't need to give this function an access to the object its no use giving this

        function access to the object.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(
            f"""`help` prints a list of commands that the Linkedin Automater have.""")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    def get_command_lenght(self):
        """
        Method get_command_lenght() returns the lenght of the command entered.

        We first change the entered string to a list object by spliting the

        string on ' ' (whitespaces) then we return the lenght.

        ! return:
            * lenght of the command entered.
        """
        return len(self.command.split(" "))

    def get_command_at_index(self, index):
        """
        Method get_command_at_index() returns a value at a given index of the command

        after changing the string to a list object. We also use strip() function to

        cut all the leading and trailing whitespaces.
        """
        return self.command.split(" ")[index].strip()

    def get_search_query(self):
        querry = self.get_command_at_index(4)

        if len(querry.split("&&")) == 2:
            if "industry=" in querry.split("&&")[0] and "location=" in querry.split("&&")[1]:
                return True
        return False

    def handle_send_commands(self):
        if self.get_command_lenght() >= 5:

            if self.get_command_at_index(3) == "suggestions" and \
                    (self.get_command_at_index(4) == "--auto" or self.get_command_at_index(4) == "--guided"):

                self.data["headless"] = True if self.get_command_lenght() >= 6 and \
                    self.get_command_at_index(5) == "--headless" else False

                if self.data["user_email"] and self.data["user_password"]:
                    pass
                else:
                    Main._print(f"""{Main.style("bright")}""", end="")
                    Main._print(f"""{Main.colorFore("blue")}""", end="")

                    Main._print(
                        f"""Need credentials first use config.user.email/password to add them.""")

                    Main._print(f"""{Main.colorFore("reset")}""", end="")
                    Main._print(f"""{Main.style("reset")}""", end="")
            elif self.get_command_at_index(3) == "search" and self.get_search_query() and \
                    (self.get_command_at_index(5) == "--auto" or self.get_command_at_index(5) == "--guided"):

                self.data["headless"] = True if self.get_command_lenght() >= 7 and \
                    self.get_command_at_index(6) == "--headless" else False

                if self.data["user_email"] and self.data["user_password"]:
                    pass
                else:
                    Main._print(f"""{Main.style("bright")}""", end="")
                    Main._print(f"""{Main.colorFore("blue")}""", end="")

                    Main._print(
                        f"""Need credentials first use config.user.email/password to add them.""")

                    Main._print(f"""{Main.colorFore("reset")}""", end="")
                    Main._print(f"""{Main.style("reset")}""", end="")

    def handle_invitation_manager_commands(self):
        pass

    def handle_mynetwork_commands(self):
        pass

    def handle_linkedin_commands(self):
        """
        Method handle_linkedin_commands() calls the main LinkedIn classes according to

        the commands given by the user, it checks the flags that are applied with the

        `linkedin` command and calls the LinkedIn classes accordingly.
        """
        if self.get_command_lenght() == 2 and self.get_command_at_index(1) == "linkedin":
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("blue")}""", end="")

            Main._print(
                f"""\n Command 'linkedin' cannot be referenced without a flag\n""")

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")

            Main.help_with_linkedin()
        elif self.get_command_lenght() >= 3:
            if self.get_command_at_index(2) == "send":
                self.handle_send_commands()
            elif self.get_command_at_index(2) == "invitation-manager":
                self.handle_invitation_manager_commands()
            elif self.get_command_at_index(2) == "mynetwork":
                self.handle_mynetwork_commands()
            elif self.get_command_at_index(2 == "--help"):
                Main.help_with_linkedin()
            else:
                Main._print(
                    f"""'{self.get_command_at_index(2)}' is not a 'linkedin' command""")
        else:
            pass

    @staticmethod
    def show_job_details(self):
        """
        Function show_job_details() prints the job details that the user entered we

        print the information about job keys once we have any of these two fields

        otherwise we don't show it. We declare this function static because we don't

        need to give this function an access to the object for just a print functionality

        its no use giving this function access to the object. Although it recieves an

        argument 'self' but it is not a object but it is a parameter object that we need

        in order to access user details.

        ! Args:
            * self: it is the parameter object that has the user details in it.
        """
        if self.data["job_keywords"] or self.data["job_location"]:
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("green")}""", end="")

            Main._print(f"""Job Keywords -> %s""" %
                        (self.data["job_keywords"] if self.data["job_keywords"] else None))
            Main._print(f"""Job Location -> %s""" %
                        (self.data["job_location"] if self.data["job_location"] else None))

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")

    @staticmethod
    def ask_to_show_password(self):
        """
        Function ask_to_show_password() asks the user if (s)he want to see the password if

        yes show them if not don't show them, this is for security purpose. We declare this

        function static because we don't need to give this function an access to the object

        for just a print functionality its no use giving this function access to the object.

        Although it recieves an argument 'self' but it is not a object but it is a parameter

        object that we need in order to access user details.

        ! Args:
            * self: it is a parameter object that has user details in it.
        """
        try:
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("blue")}""", end="")

            ch = input(
                f""" Show password anyway? [y/N]: """) if self.data["user_password"] else "n"

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")

            if ch.lower() == "y":
                Main._print(f"""{Main.style("bright")}""", end="")
                Main._print(f"""{Main.colorFore("green")}""", end="")

                Main._print(f"""%s""" % (
                    self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"))
                Main._print(f"""%s""" % (
                    self.data["user_password"] if self.data["user_password"] else "use config.user.password to add user password"))

                Main._print(f"""{Main.colorFore("reset")}""", end="")
                Main._print(f"""{Main.style("reset")}""", end="")
        except KeyboardInterrupt:
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("green")}""", end="")

            Main._print(f"""\n Piece""")

            Main._print(f"""Main.colorFore("reset")""", end="")
            Main._print(f"""Main.style("reset")""", end="")

            quit()

    def handle_show_commands(self):
        """
        Method show() gets executed once the user hit the command `show` this basically

        prints the information that user had entered like email, password, job keys/location.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(f"""%s""" % (
            self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"))
        Main._print(f"""%s""" % (
            "*"*len(self.data["user_password"]) if self.data["user_password"] else "use config.user.password to add user password"))

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

        Main.show_job_details(self)

        Main.ask_to_show_password(self)

    def handle_developer_commands(self):
        """
        Method developer() gets executed once the user hits the command `devdetails` it

        basically shows the developer's network profiles and mail address.
        """
        Main._print(f"""{Main.style("bright")}""", end="")
        Main._print(f"""{Main.colorFore("green")}""", end="")

        Main._print(f"""Name     :  Ayush Joshi""")
        Main._print(f"""Email    :  ayush854032@gmail.com (primary)""")
        Main._print(f"""Email    :  joshiayush.joshiayush@gmail.com""")
        Main._print(f"""Mobile   :  +91 8941854032 (Only WhatsApp)""")
        Main._print(f"""GitHub   :  https://github.com/JoshiAyush""")
        Main._print(
            f"""LinkedIn :  https://www.linkedin.com/in/ayush-joshi-3600a01b7/{Main.colorFore("reset")}""")

        Main._print(f"""{Main.colorFore("reset")}""", end="")
        Main._print(f"""{Main.style("reset")}""", end="")

    def handle_theme_commands(self):
        """
        Method handle_theme_commands() handles the 'theme' commands it calls the set_theme()

        function once it confirms that the flag that is given with the theme command is an

        actual theme flag. We does a lot of argument parsing in this function as you can

        see this is to fetch the right flag and if not found raise an error.
        """
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
        """
        Method handle_clear_commands() handles the 'clear' commands it calls the home()

        function once it confirms that the given command is exactly a 'clear' command,

        it also checks for the flag that is given with the 'clear' command is an actual

        'clear' flag. We does a lot of argument parsing in this function as you can see

        this is to fetch the right flag and if not found raise an error.
        """
        if self.get_command_lenght() == 2 and self.get_command_at_index(1) == "clear":
            self.home()
        elif self.get_command_lenght() >= 3 and self.get_command_at_index(2) == "--help":
            Main.help_with_clear()
            if self.get_command_lenght() > 3:
                self.command = (
                    "command " + self.get_command_at_index(3)).strip()
                self.Error()
        else:
            pass

    def handle_help_commands(self):
        """
        Method hanlde_help_commands() handles the 'help' command it provides a manual to the

        user if it identifies that the given command is an actual help command, this guide

        contains every information that a user needs in order to start linkedin automation.

        We does a lot of argument parsing in this function as you can see this is to fetch the

        right flag and if not found raise an error.
        """
        if self.get_command_lenght() == 2 and self.get_command_at_index(1) == "help":
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("green")}""", end="")

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
                f"""linkedin [invitation-manager*] [ignore*/withdraw*] [all*^/over > <days>*] [--headless]""")
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

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")
        elif self.get_command_lenght() >= 3 and self.get_command_at_index(2) == "--help":
            Main.help_with_help()
            if self.get_command_lenght() > 3:
                self.command = (
                    "command " + self.command.split(" ")[3]).strip()
                self.Error()
        else:
            pass

    def handle_exit_commands(self):
        """
        Method handle_exit_commands() handles the 'exit' commands it calls the python's

        exit() function once it confirms that the given command is exactly a 'exit' command,

        it also checks for the flag that is given with the 'exit' command is an actual

        'exit' flag. We does a lot of argument parsing in this function as you can see

        this is to fetch the right flag and if not found raise an error.
        """
        if self.get_command_lenght() == 2 and self.get_command_at_index(1) == "exit":
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("green")}""", end="")

            Main._print(f"""Piece""")

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")
            exit()
        elif self.get_command_lenght() >= 3 and self.get_command_at_index(2) == "--help":
            Main.help_with_exit()
            if self.get_command_lenght() > 3:
                self.command = (
                    "command " + self.get_command_at_index(3)).strip()
                self.Error()
        else:
            pass

    def Error(self):
        """
        Method Error() gets called when the entered command is not recognized. We say

        'self.command[8:]' because this way we are triming the 'command ' from the

        entered command because we don't want to confuse the user by showing him/her

        what is going in the background.
        """
        if self.command:
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("red")}""", end="")

            Main._print(
                f"""`{self.command[8:]}` is not recognized as an internal command.""")

            Main._print(f"""{Main.colorFore("reset")}""", end="")
            Main._print(f"""{Main.style("reset")}""", end="")

    def check_email(self):
        if re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", self.command[self.command.find("=")+1:].strip()):
            return True
        elif re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$", self.command[self.command.find("=")+1:].strip()):
            return True
        else:
            return False

    def handle_configs(self):
        """
        Method handle_configs() basically saves the user's configurations that are passed

        by hitting the command `config.user.email/password` or `config.job/keywords/location`.

        We use re.compile() and re.search() method here to find the pattern in the command.

        We does a lot of argument parsing in this function as you can see this is to fetch

        the right commands and flags and if not found raise an error.
        """
        if "config.user.password" == self.get_command_at_index(1):
            self.data["user_password"] = getpass.getpass(prompt=" Password: ")

        elif re.compile(r"(config\.user\.email)=\w+", re.IGNORECASE).search(self.command):
            if self.check_email():
                self.data["user_email"] = self.command[self.command.find(
                    "=")+1:].strip()
            else:
                Main._print(f"""{Main.style("bright")}""", end="")
                Main._print(f"""{Main.colorFore("red")}""", end="")

                Main._print(
                    f"""'{self.command[self.command.find("=")+1:].strip()}' is not a valid email address!""")

                Main._print(f"""{Main.colorFore("rest")}""", end="")
                Main._print(f"""{Main.style("reset")}""", end="")

        elif re.compile(r"(config\.job\.keywords)=\w+", re.IGNORECASE).search(self.command):
            self.data["job_keywords"] = self.command[self.command.find(
                "=")+1:].strip()

        elif re.compile(r"(config\.job\.location)=\w+", re.IGNORECASE).search(self.command):
            self.data["job_location"] = self.command[self.command.find(
                "=")+1:].strip()

        else:
            Main.help_with_configs()

    def handle_commands(self):
        """
        Method handle_commands() does the actually handling of the commands entered, we first

        find pattern for 'configuration' commands using the re.compile() and re.search() method,

        which finds the pattern in the entered command and calls 'handle_configs()' method if it

        finds any match if not it calls the functions according to the commands entered and if

        still does not find any function call for the entered command it just hits the self.Error()

        method.
        """
        _config_regex_ = re.compile(
            r"(config\.user\.email).?(\w+)?|(config\.user\.password)|(config\.job\.keywords).?(\w+)?|(config\.job\.location).?(\w+)?", re.IGNORECASE)

        if _config_regex_.search(self.get_command_at_index(1)):
            self.handle_configs()

        else:
            # ? get() method of dictionary data type returns
            # ? value of passed argument if it is present
            # ? in dictionary otherwise second argument will
            # ? be assigned as default value of passed argument.
            self.commands.get(self.command.split(" ")[1], self.Error)()

    def run(self):
        """
        Method run() runs a infinite loop and starts the `cli` (Command Line Interface) and

        it actually starts listening to the commands and then it calls the function handle_commands()

        which handles the commands.
        """
        while True:
            # ? get the command and add 'command ' in it this way we
            # ? can handle the commands situated at list indices.
            self.command = ("command " + self._input()).strip()
            # ? calling function handle commands that is going to
            # ? perform operations as per command
            self.handle_commands() if self.get_command_lenght() > 1 else False


# ! Execute program
if __name__ == "__main__":
    Main().run()

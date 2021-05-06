import re
import os
import sys
import getpass
import colorama
from cryptography.fernet import Fernet

# importing `readline` this we need to import becuase when
# we take input from the terminal window and we press arrow
# keys then the characters that corresponds to the pressed
# key gets printed and we don't need that we need the cursor
# moving on pressing arrow keys.
import readline

from helpers.print import printk
from helpers.print import printRed
from helpers.print import printBlue
from helpers.print import printGreen

from linkedin.LinkedInConnectionsAuto import LinkedInConnectionsAuto
from linkedin.LinkedInConnectionsGuided import LinkedInConnectionsGuided


class Main(object):
    """Class Main is the main class that gets executed after the user
    hits the command `./run.sh` on the terminal screen, this class gives
    the `cli` (Command Line Interface) to the user. We don't have `GUI`
    (Graphical User Interface) here because I don't have any deign Idea
    in my mind yet.

    Class Variable:
        THEME: is the theme for our cli (command line interface).
    """
    PARROT = True

    def __init__(self):
        """Method __init__() initializes the commands and required variables,
        it also prints the Logo on the screen it calls method init_commands()
        that initializes all the commands that we can have in this program then
        it calls the init_vars() method to initialize the variables required
        then it calls method home() to print a sexy logo on the screen.
        """
        self.init_commands()

        self.init_vars()

        self.home()

    def init_commands(self):
        """Method init_commands() initialize the commands that LinkedIn
        Automater provides for now we have following commands,

        Commands:
            * config     : shows how you can add fields
            * linkedin   : activates the automation process
            * show       : shows the entered details
            * delete     : deletes the cache stored
            * developer  : prints the developer details
            * theme      : sets the given theme
            * clear      : clears the screen
            * help       : prints the commands and their usage
            * exit       : exit from the program
        """
        self.commands = {
            "config": self.handle_config,
            "linkedin": self.handle_linkedin_commands,
            "show": self.handle_show_commands,
            "delete": self.handle_delete_commands,
            "developer": self.handle_developer_commands,
            "theme": self.handle_theme_commands,
            "clear": self.handle_clear_commands,
            "help": self.handle_help_commands,
            "exit": self.handle_exit_commands,
        }

    def init_vars(self):
        """Method init_vars() intialize the dictionary that holds the
        user's details like credentials and jobs search, etc, it also
        initializes a dictionary which conatins commands and their
        corresponding help functions, there's one more variable that
        gets initializes that is the theme variable for our cli
        (Command Line Interface).
        """
        self.encrypted_email = ""

        self.encrypted_password = ""

        self.__key_file = "/Python/linkedin-bot/creds/.key.key"

        if not os.path.exists(self.__key_file):
            self.__key = Fernet.generate_key()

            with open(self.__key_file, 'w') as key_file:
                key_file.write(self.__key.decode())
        else:
            with open(self.__key_file, 'r') as key_file:
                self.__key = key_file.readline().encode()

        self.__credentials_file = "/Python/linkedin-bot/creds/credentialsFile.ini"

        self.data = {
            "user_email": "",
            "user_password": "",
            "search_keywords": "",
            "search_location": "",
            "job_keywords": "",
            "job_location": "",
            "driver_path": "/Python/linkedin-bot/driver/chromedriver",
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

    def encrypt_email(self):
        """Method encrypt_email() encrypts the user email so
        to store this field as a cache later. We use 'Fernet'
        class to encrypt user password.

            Fernet:
            Fernet guarantees that a message encrypted using it cannot
            be manipulated or read without the key. Fernet is an
            implementation of symmetric (also known as “secret key”)
            authenticated cryptography.
        """
        fernet = Fernet(self.__key)

        self.encrypted_email = fernet.encrypt(
            self.data["user_email"].encode()).decode()

        del fernet

    def encrypt_password(self):
        """Method encrypt_password() encrypts the user password so
        to store this field as a cache later. We use 'Fernet' class
        to encrypt user password.

        Fernet:
            Fernet guarantees that a message encrypted using it cannot
            be manipulated or read without the key. Fernet is an
            implementation of symmetric (also known as “secret key”)
            authenticated cryptography.
        """
        fernet = Fernet(self.__key)

        self.encrypted_password = fernet.encrypt(
            self.data["user_password"].encode()).decode()

        del fernet

    def decrypt_credentials(self, config):
        """Method decrypt_credentials() decrypts the encrypted user
        credentials that are stored in the Credentials file. We use
        class 'Fernet' to achive this functionality.

        Fernet:
            Fernet guarantees that a message encrypted using it cannot
            be manipulated or read without the key. Fernet is an
            implementation of symmetric (also known as “secret key”)
            authenticated cryptography.

        Args:
            config: it is a dictionary object that holds user encrypted
            fields.
        """
        fernet = Fernet(self.__key)

        self.data["user_email"] = fernet.decrypt(
            config["Username"].encode('utf-8')).decode('utf-8')
        self.data["user_password"] = fernet.decrypt(
            config["Password"].encode('utf-8')).decode('utf-8')

    def store_credentials(self):
        """Method store_credentials() stores the user secret fields
        as cache in a file 'CredentialsFile.ini' so to use these
        fields later.
        """
        with open(self.__credentials_file, 'w') as creds_file:
            creds_file.write("Username={}\nPassword={}\n".format(
                self.encrypted_email, self.encrypted_password))

    def get_credentials(self):
        """Method get_credentials() reads the credentials stored as
        cache in file 'CredentialsFile.ini' if exists.
        """
        if os.path.exists(self.__credentials_file):
            try:
                with open(self.__credentials_file, 'r') as creds_file:
                    lines = creds_file.readlines()

                    config = {
                        "Username": "",
                        "Password": ""
                    }

                    for line in lines:
                        creds = line.rstrip('\n').split('=', 1)
                        if creds[0] in ("Username", "Password"):
                            config[creds[0]] = creds[1]

                    self.decrypt_credentials(config)
                    return True
            except FileNotFoundError:
                return False

        printRed(f"""You don't have any cache stored.""", style='b', pad='1')

        Main.help_with_configs()

        return False

    def store_cache(self):
        """Method store_cache() applies encryption on the fields if both
        the fields are available and the calls the method 'store_credentials'
        to store the credentials as cache.
        """
        if self.data["user_email"] and self.data["user_password"]:
            self.encrypt_email()
            self.encrypt_password()
            self.store_credentials()

    @staticmethod
    def terminal_size():
        """Function terminal_size() returns the size of the terminal when
        the LinkedIn Automator program executed, this functionality is required
        in order to set the Home Logo according to the terminal size. We declare
        this method static because we don't need to give this function an access
        to the object it's no use giving this function access to the object.

        return:
            terminal size.
        """
        return os.get_terminal_size()

    @staticmethod
    def get_coords():
        """Function get_coords() returns the co-ordinates that are needed to set
        the Home Logo nearly to the center according to the terminal size. We
        declare this function static because we don't need to give this function
        an access to the object it's no use giving this function access to the object.

        return:
            co-ordinates that sets the Logo nearly to the center.
        """
        if Main.terminal_size()[0] >= 150:
            return [48, 5]
        elif Main.terminal_size()[0] >= 80:
            return [15, 2]
        else:
            return [15, 2]

    @staticmethod
    def gotoxy(x, y):
        """Function gotoxy() sets the console cursor position. We declare this
        function static because we don't need to give this function an access
        to the object it's no use giving this function access to the object.

        Args:
            x: column number for the cursor.
            y: row number for the cursor.
        """
        print("%c[%d;%df" % (0x1B, y, x), end='')

    @staticmethod
    def style(style):
        """Function style() returns the text style that we are printing on the
        terminal, it uses 'colorama' module to generate unicode for the given
        style value. We declare this function static because we don't need to
        give this function an access to the object it's no use giving this
        function access to the object.

        Args:
            style: it is the style to be given to the text on the screen.

        return:
            text style.
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
        """Function colorFore() returns the text color according to the theme
        enabled, it returns the text color only if the theme is set to '--parrot'
        otherwise it only returns a unicode for color 'red' or 'reset' command if
        the theme is set to '--normal'. We declare this function static because
        we don't need to give this function an access to the object it's no use
        giving this function access to the object.

        Args:
            color: it is the color that we need to return the unicode for.

        return:
            unicode for color.
        """
        colors = {
            "red": colorama.Fore.RED,
            "green": colorama.Fore.GREEN,
            "blue": colorama.Fore.BLUE,
            "reset": colorama.Fore.RESET
        }

        if Main.PARROT:
            return colors.get(color, colorama.Fore.RESET)
        else:
            return colors.get(color, colorama.Fore.RESET) if color == "red" or color == "reset" else " \b"

    def clear(self):
        """Method clear() clears the terminal screen for windows we use command
        `cls` and for linux based system we use command `clear`.
        """
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')

    def home(self):
        """Method home() prints the home screen.

        First it clears the screen using the method clear().
        """
        self.clear()

        printGreen(f"""Type help for more information!""",
                   style='b', start='\n', pad='1')

    def set_theme(self, _theme):
        """Function set_theme() sets the cli (Command Line Interface) theme
        according to the value given.

        Args:
            _theme: it is the theme that the we need to give to our cli after
            user has entered it.
        """
        if _theme == "--parrot":
            Main.PARROT = True
            self.home()
        elif _theme == "--normal":
            Main.PARROT = False
            self.home()
        else:
            Main._print(
                f"""'{_theme}' can't be recognized as a 'theme' command""")

    @staticmethod
    def help_with_configs():
        """Function help_with_configs()
        """
        printBlue(f"""config.user.email "example@email.com" --cached""",
                  style='b', pad='1')
        printBlue(
            f"""config.user.password "example@password" --cached""", style='b', pad='1')
        printBlue(
            f"""Or you can use the following command if you don't want to show the password on the screen""",
            style='b', pad='1')
        printBlue(f"""config.user.password --cached (hit enter)""",
                  style='b', pad='1')
        printBlue(f"""Password: """, style='b', pad='1')
        printBlue(
            f"""config.job.keywords "Data%Science" (use '%' for space)""", style='b', pad='1')
        printBlue(f"""config.job.location "Sanfrancisco%CA" """,
                  style='b', pad='1')

    @staticmethod
    def help_with_linkedin():
        """Method help_with_linkedin() shows how you can use the linkedin
        command in case you missed the flags with the linkedin command or
        mistakenly applied wrong flags with the linkedin command. We declare
        this function static because we don't need to give this function an
        access to the object it's no use giving this function access to the
        object.
        """
        printBlue(
            f"""linkedin [send] [suggestions^] --auto/--guided [--headless] [--use-cache]""", style='b', pad='1')
        printBlue(
            f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
        printBlue(
            f"""'send' flag sends invitations according to the path given to it.""", style='b', pad='1')
        printBlue(
            f"""'suggestions' flag lets linkedin know that it must use""", style='b', pad='1')
        printBlue(f"""'MyNetwork' tab as a target.""", style='b', pad='1')
        printBlue(
            f"""'--auto/--guided' flag tells the linkedin to start process in auto(recommended) or guided mode.""",
            style='b', pad='1')
        printBlue(
            f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
        printBlue(
            f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
        printBlue(
            f"""linkedin [send] [search industry=example&&location=india+usa+...] --auto^/--guided [--headless]""", start='\n', style='b', pad='1')
        printBlue(
            f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
        printBlue(
            f"""'send' flag sends invitations according to the path given to it.""", style='b', pad='1')
        printBlue(
            f"""'search industry=example&&location=india+usa+...' flag lets linkedin know that it must""", style='b', pad='1')
        printBlue(
            f"""go and search for people associated to the given industry (use (%) for space between words in industry)""",
            style='b', pad='1')
        printBlue(
            f"""and living in the given location. You can always add location.""", style='b', pad='1')
        printBlue(
            f"""'--auto/--guided' flag tells the linkedin to start process in auto(recommended) or guided mode.""",
            style='b', pad='1')
        printBlue(
            f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
        printBlue(
            f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
        printBlue(
            f"""linkedin [invitation-manager*] [show*] --sent*/--recieved* [--headless]""", start='\n', style='b', pad='1')
        printBlue(
            f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
        printBlue(
            f"""'invitation-manager' flag tells the linkedin to start performing operations on""", style='b', pad='1')
        printBlue(f"""invitation manager tab.""", style='b', pad='1')
        printBlue(
            f"""'show' flag show tells the linkedin to show the people my account want to connect with.""", style='b', pad='1')
        printBlue(
            f"""'--sent/--recieved' flag tells the linkedin to fetch either sent invitations or recieved ones.""",
            style='b', pad='1')
        printBlue(
            f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
        printBlue(
            f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
        printBlue(
            f"""linkedin [invitation-manager*] [ignore*/withdraw*] [all*^/over > <days>*] [--headless]""",
            start='\n', style='b', pad='1')
        printBlue(
            f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
        printBlue(
            f"""'invitation-manager' flag tells the linkedin to start performing operations on""", style='b', pad='1')
        printBlue(
            f"""'ignore/withdraw' flag tells the linkedin that you want to activate invitation ignoring or withdrawing process.""",
            style='b', pad='1')
        printBlue(
            f"""'all/over > <days>' flag tell to either withdraw all the sent invitations or""", style='b', pad='1')
        printBlue(
            f"""use the amount of days given to withdraw sent invitations accordingly.""", style='b', pad='1')
        printBlue(
            f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
        printBlue(
            f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
        printBlue(
            f"""linkedin [mynetwork*] [show*] [all*/page > 1^+2+3+...*] [--headless]""", start='\n', style='b', pad='1')
        printBlue(
            f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
        printBlue(
            f"""'mynetwork' flag tell the linkedin to start operating on MyNetworks.""", style='b', pad='1')
        printBlue(
            f"""'all/page > 1+2+3+...' flag tells either show all connections or use the pages given.""", style='b', pad='1')
        printBlue(
            f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
        printBlue(
            f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')
        printBlue(
            f"""linkedin [mynetwork*] [sendmessage*] [all*] [--greet*^] [--headless]""", start='\n', style='b', pad='1')
        printBlue(
            f"""'linkedin' command handles the linkedin process.""", style='b', pad='1')
        printBlue(
            f"""'mynetwork' flag tell the linkedin to start operating on MyNetworks.""", style='b', pad='1')
        printBlue(
            f"""'sendmessage' flag tells the linkedin to send messages to connections.""", style='b', pad='1')
        printBlue(
            f"""'all' flag tells the linkedin to use all connections.""", style='b', pad='1')
        printBlue(
            f"""'--greet' flag tells the linkedin to send greet message.""", style='b', pad='1')
        printBlue(
            f"""'--headless' flag tells the program to start automation without opening the browser.""", style='b', pad='1')
        printBlue(
            f"""'--use-cache' uses cache (if stored) for authentication.""", style='b', pad='1')

    @staticmethod
    def help_with_show():
        """Function help_with_show() shows you how you can use the
        'show' command in case you entered wrong command. We declare
        this function static because we don't need to give this function
        an access to the object it's no use giving this function access
        to the object.
        """
        printBlue(
            f"""'show' shows all the details you have entered like:""", style='b', pad='1')
        printBlue(f"""user.email,""", style='b', pad='1')
        printBlue(
            f"""user.password (asks first if you want to see it really or not),""", style='b', pad='1')
        printBlue(f"""job.keywords,""", style='b', pad='1')
        printBlue(f"""job.location""", style='b', pad='1')

    @staticmethod
    def help_with_delete():
        printBlue(f"""'delete' command deletes the cache stored.""",
                  style='b', pad='1')
        printBlue(f"""Usage: delete --cache""", style='b', pad='1')

    @staticmethod
    def help_with_developer():
        """Function help_with_developer() shows you how you can use the
        'developer' command in case you entered wrong command. We declare
        this function static because we don't need to give this function
        an access to the object it's no use giving this function access to
        the object.
        """
        printBlue(f"""'developer' shows the developer details like:""",
                  style='b', pad='1')
        printBlue(f"""his number, email, profiles ...""", style='b', pad='1')

    @staticmethod
    def help_with_theme():
        """Function help_with_theme() shows you how you can use the
        'theme' command in case you entered wrong command or entered
        a un-matching flag. We declare this function static because
        we don't need to give this function an access to the object
        it's no use giving this function access to the object.
        """
        printBlue(
            f"""'theme --parrot/--normal' changes the cli (command line theme) according to the given theme value.""",
            style='b', pad='1')

    @staticmethod
    def help_with_clear():
        """Function help_with_clear() shows you how you can use the
        'clear' command in case you entered wrong command. We declare
        this function static because we don't need to give this function
        an access to the object it's no use giving this function access
        to the object.
        """
        printBlue(f"""'clear' clears the screen""", style='b', pad='1')

    @staticmethod
    def help_with_exit():
        """Function help_with_exit() shows you how you can use the
        'exit' command in case you entered wrong command. We declare
        this function static because we don't need to give this function
        an access to the object it's no use giving this function access
        to the object.
        """
        printBlue(
            f"""'exit' exits the program and also does flushing jobs.""", style='b', pad='1')

    @staticmethod
    def help_with_help():
        """Function help_with_help() shows you how you can use the
        'help' command in case you entered wrong command. We declare
        this function static because we don't need to give this function
        an access to the object it's no use giving this function access
        to the object.
        """
        printBlue(
            f"""'help' prints a list of commands that the Linkedin Automater have.""",
            style='b', pad='1')

    def handle_config(self):
        Main.help_with_configs()

    def get_command_length(self):
        """Method get_command_length() returns the lenght of the command
        entered. We first change the entered string to a list object by
        spliting the string on ' ' (whitespaces) then we return the lenght.

        return:
            lenght of the command entered.
        """
        return len(self.command.split(" "))

    def get_command_at_index(self, index):
        """Method get_command_at_index() returns a value at a given index
        of the command after changing the string to a list object. We also
        use strip() function to cut all the leading and trailing whitespaces.
        """
        try:
            return self.command.split(" ")[index].strip()
        except IndexError:
            return None

    def get_search_query(self):
        querry = self.get_command_at_index(4)

        if len(querry.split("&&")) == 2:
            if "industry=" in querry.split("&&")[0] and (True or "location=" in querry.split("&&")[1]):
                self.data["search_keywords"] = querry.split(
                    "&&")[0][querry.split("&&")[0].find("=")+1::]
                if "location" in querry.split("&&")[1]:
                    self.data["search_location"] = querry.split(
                        "&&")[1][querry.split("&&")[1].find("=")+1::]
                    return True
                return True

        return False

    @staticmethod
    def no_credentials():
        printBlue(
            f"""Need credentials first use config.user.email/password to add them.""",
            style='b', pad='1')

    def handle_send_commands(self):
        """Method handle_send_commands() handles the operations when you
        apply flag 'send' with 'linkedin' command. We handle operation in
        two ways where one is when the user enters exact number of flags
        with these commands and the other is when user ommits the default
        flags.

        Usage:
            -> linkedin [send] [suggestions^] --auto^/--guided [--headless] [--use--cache]

            -> linkedin [send] [search industry=example&&location=india+usa+...] --auto^/--guided [--headless] [--use-cache]
        """
        if self.get_command_at_index(2) == "send":
            """If user entered command with exact number of flags required
            with that command then we perform the following operations where
            we take actions according to the flags 'suggestions' or 'search'
            in this case the parsing of arguments is done by targetting their
            positions, remember flag 'suggestions' is default means even if
            the user ommits it linkedin must go to the suggestion box to send
            invitations to people and the flag '--auto' is also a default flag
            in case user omits it linkedin should start the process in auto
            mode.
            """
            if self.get_command_at_index(-1) == "--use-cache":
                self.get_credentials()

            if self.get_command_at_index(-2) == "--headless":
                self.data["headless"] = True

            if self.get_command_at_index(3) == "suggestions":
                if self.get_command_at_index(4) == "--guided":
                    if self.data["user_email"] and self.data["user_password"]:
                        LinkedInConnectionsGuided(self.data).run()
                    else:
                        Main.no_credentials()
                    return
                else:
                    if self.data["user_email"] and self.data["user_password"]:
                        LinkedInConnectionsAuto(self.data).run()
                    else:
                        Main.no_credentials()
                    return
            elif self.get_command_at_index(3) == "--headless" or self.get_command_at_index(3) == "--use-cache":
                if self.data["user_email"] and self.data["user_password"]:
                    LinkedInConnectionsAuto(self.data).run()
                else:
                    Main.no_credentials()
                return
            elif self.get_command_length() == 3:
                if self.data["user_email"] and self.data["user_password"]:
                    LinkedInConnectionsAuto(self.data).run()
                else:
                    Main.no_credentials()
                return
            else:
                self.command = self.command[3:]
                self.handle_commands()
                return

    def handle_invitation_manager_commands(self):
        pass

    def handle_mynetwork_commands(self):
        pass

    def handle_linkedin_commands(self):
        """Method handle_linkedin_commands() calls the main LinkedIn
        classes according to the commands given by the user, it checks
        the flags that are applied with the `linkedin` command and calls
        the LinkedIn classes accordingly.
        """
        if self.get_command_length() <= 2 and self.get_command_at_index(1) == "linkedin":
            printBlue(f"""Command 'linkedin' cannot be referenced without a flag\n""",
                      style='b', start='\n', end='\n', pad='1')

            Main.help_with_linkedin()

        elif self.get_command_length() >= 3:

            if self.get_command_at_index(2) == "send":
                self.handle_send_commands()

            elif self.get_command_at_index(2) == "invitation-manager":
                self.handle_invitation_manager_commands()

            elif self.get_command_at_index(2) == "mynetwork":
                self.handle_mynetwork_commands()

            elif self.get_command_at_index(2 == "--help"):
                Main.help_with_linkedin()

            else:
                printRed(
                    f"""'{self.get_command_at_index(2)}' is not a 'linkedin' command""", style='b', pad='1')

        else:
            Main.help_with_linkedin()

    @staticmethod
    def show_job_details(self):
        """Function show_job_details() prints the job details that the
        user entered we print the information about job keys once we have
        any of these two fields otherwise we don't show it. We declare this
        function static because we don't need to give this function an access
        to the object for just a print functionality it's no use giving this
        function access to the object. Although it recieves an argument 'self'
        but it is not a object but it is a parameter object that we need in
        order to access user details.

        Args:
            self: it is the parameter object that has the user details in it.
        """
        if self.data["job_keywords"] or self.data["job_location"]:
            printGreen(f"""Job Keywords -> %s""" %
                       (self.data["job_keywords"]
                        if self.data["job_keywords"] else None),
                       style='b', pad='1')
            printGreen(f"""Job Location -> %s""" %
                       (self.data["job_location"]
                        if self.data["job_location"] else None),
                       style='b', pad='1')

    @staticmethod
    def ask_to_show_password(self):
        """Function ask_to_show_password() asks the user if (s)he want
        to see the password if yes show them if not don't show them,
        this is for security purpose. We declare this function static
        because we don't need to give this function an access to the
        object for just a print functionality it's no use giving this
        function access to the object. Although it recieves an argument
        'self' but it is not a object but it is a parameter object that
        we need in order to access user details.

        Args:
            self: it is a parameter object that has user details in it.
        """
        try:
            printk(f"""{Main.style("bright")}""", end="")
            printk(f"""{Main.colorFore("blue")}""", end="")

            ch = input(
                f""" Show password anyway? [y/N]: """) if self.data["user_password"] else "n"

            printk(f"""{Main.colorFore("reset")}""", end="")
            printk(f"""{Main.style("reset")}""", end="")

            if ch.lower() == "y":
                printGreen(f"""%s""" % (
                    self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"),
                    style='b', pad='1')
                printGreen(f"""%s""" % (
                    self.data["user_password"] if self.data["user_password"] else "use config.user.password to add user password"),
                    style='b', pad='1')
        except KeyboardInterrupt:
            printGreen(f"""Piece""", start='\n', pad='1')

            sys.exit()

    def handle_show_commands(self):
        """Method show() gets executed once the user hit the
        command `show` this basically prints the information
        that user had entered like email, password, job
        keys/location.
        """
        if self.get_command_length() == 2:
            printGreen(f"""%s""" % (
                self.data["user_email"] if self.data["user_email"] else "use config.user.email to add user email"),
                style='b', pad='1')
            printGreen(f"""%s""" % (
                "*"*len(self.data["user_password"]) if self.data["user_password"] else "use config.user.password to add user password"),
                style='b', pad='1')

            Main.show_job_details(self)
            Main.ask_to_show_password(self)
        elif self.get_command_at_index(2) == "--help":
            Main.help_with_show()
        else:
            Main.help_with_show()

    def delete_cache(self):
        """Method delete_cache() deletes the stored cache (User credentials)
        if exists, we use os.path.exists() to check if the file is present or
        not if present we remove it.
        """
        if os.path.exists(self.__credentials_file):
            os.remove(self.__credentials_file)
        else:
            printRed(f"""There's no credential file exists to delete.""",
                     style='b', pad='1')

    def delete_key(self):
        """Method delete_key() deletes the stored cipher key if exists,
        we use os.path.exists() to check if the file is present or not if
        present we remove it.
        """
        if os.path.exists(self.__key_file):
            os.remove(self.__key_file)
        else:
            printRed(f"""There's no key file exists to delete.""",
                     style='b', pad='1')

    def handle_delete_commands(self):
        """Method handle_delete_commands() gets executed once
        the user hits the command `delete` this basically deletes
        the cache stored (User credentials) if exists.
        """
        if self.get_command_at_index(1) == "delete":
            printRed(f"""command 'delete' cannot be reference alone.""",
                     style='b', pad='1')
            Main.help_with_delete()
        elif self.get_command_length() >= 3:
            if self.get_command_at_index(2) == "--cache":
                self.delete_cache()
            elif self.get_command_at_index(2) == "--key":
                self.delete_key()
            elif self.get_command_at_index(2) == "--help":
                Main.help_with_delete()
            elif self.get_command_at_index(2) == "--cache&&--key":
                self.delete_cache()
                self.delete_key()
            else:
                printRed(
                    f"""flag '{self.get_command_at_index(2)}' is not recognized.""", style='b', pad='1')
        else:
            Main.help_with_delete()

    def handle_developer_commands(self):
        """Method developer() gets executed once the user hits
        the command `devdetails` it basically shows the developer's
        network profiles and mail address.
        """
        if self.get_command_length() == 2:
            Main._print(f"""{Main.style("bright")}""", end="")
            Main._print(f"""{Main.colorFore("green")}""", end="")

            printGreen(f"""Name     :  Ayush Joshi""", style='b', pad='1')
            printGreen(
                f"""Email    :  ayush854032@gmail.com (primary)""", style='b', pad='1')
            printGreen(
                f"""Email    :  joshiayush.joshiayush@gmail.com""", style='b', pad='1')
            printGreen(
                f"""Mobile   :  +91 8941854032 (Only WhatsApp)""", style='b', pad='1')
            printGreen(
                f"""GitHub   :  https://github.com/JoshiAyush""", style='b', pad='1')
            printGreen(
                f"""LinkedIn :  https://www.linkedin.com/in/ayush-joshi-3600a01b7/{Main.colorFore("reset")}""",
                style='b', pad='1')
        elif self.get_command_at_index(2) == "--help":
            Main.help_with_developer()
        else:
            pass

    def handle_theme_commands(self):
        """Method handle_theme_commands() handles the 'theme' commands
        it calls the set_theme() function once it confirms that the flag
        that is given with the theme command is an actual theme flag. We
        does a lot of argument parsing in this function as you can see
        this is to fetch the right flag and if not found raise an error.
        """
        if self.get_command_at_index(2) == "--help":
            Main.help_with_theme()
            if self.get_command_length() > 3:
                self.command = (
                    "command " + self.get_command_at_index(3)).strip()
                self.Error()
        elif self.get_command_at_index(2) == "--parrot" or self.get_command_at_index(2) == "--normal":
            self.set_theme(self.get_command_at_index(2).strip())
        else:
            Main.help_with_theme()

    def handle_clear_commands(self):
        """Method handle_clear_commands() handles the 'clear' commands
        it calls the home() function once it confirms that the given
        command is exactly a 'clear' command, it also checks for the flag
        that is given with the 'clear' command is an actual 'clear' flag.
        We does a lot of argument parsing in this function as you can see
        this is to fetch the right flag and if not found raise an error.
        """
        if self.get_command_at_index(1) == "clear":
            self.home()
        elif self.get_command_at_index(2) == "--help":
            Main.help_with_clear()
            if self.get_command_length() > 3:
                self.command = (
                    "command " + self.get_command_at_index(3)).strip()
                self.Error()
        else:
            Main.help_with_clear()

    def handle_help_commands(self):
        """Method hanlde_help_commands() handles the 'help' command
        it provides a manual to the user if it identifies that the
        given command is an actual help command, this guide contains
        every information that a user needs in order to start linkedin
        automation. We does a lot of argument parsing in this function
        as you can see this is to fetch the right flag and if not found
        raise an error.
        """
        if self.get_command_at_index(1) == "help":
            printGreen(
                f"""LinkedIn Bash, version 1.0.0(1)-release (lnkdbt-1.0.0)""", style='b', pad='1')
            printGreen(
                f"""These commands are defined internally. Type 'help' to see this list.""", style='b', pad='1')
            printGreen(
                f"""Type 'command' --help to know more about that command.""", style='b', pad='1')
            printGreen(
                f"""A ([]) around a command means that the command is optional.""", start='\n', style='b', pad='1')
            printGreen(
                f"""A (^) next to command means that the command is the default command.""", style='b', pad='1')
            printGreen(
                f"""A (<>) around a name means that the field is required.""", style='b', pad='1')
            printGreen(
                f"""A (/) between commands means that you can write either of these but not all.""", style='b', pad='1')
            printGreen(
                f"""A (*) next to a name means that the command is disabled.""", style='b', pad='1')
            printGreen(
                f"""linkedin [send] [suggestions^] --auto^/--guided [--headless] [--use-cache]""",
                start='\n', style='b', pad='1')
            printGreen(
                f"""linkedin [send] [search industry=example&&location=india+usa+...] --auto^/--guided [--headless] [--use-cache]""",
                style='b', pad='1')
            printGreen(
                f"""linkedin [invitation-manager*] [show*] --sent*^/--recieved* [--headless] [--use-cache]""", style='b', pad='1')
            printGreen(
                f"""linkedin [invitation-manager*] [ignore*/withdraw*] [all*^/over > <days>*] [--headless] [--use-cache]""",
                style='b', pad='1')
            printGreen(
                f"""linkedin [mynetwork*] [show*] [all*^/page > 1^+2+3+...*] [--headless] [--use-cache]""", style='b', pad='1')
            printGreen(
                f"""linkedin [mynetwork*] [sendmessage*] [all*^] [--greet*^] [--headless] [--use-cache]""", style='b', pad='1')
            printGreen(f"""config""",
                       style='b', pad='1', start='\n')
            printGreen(f"""show""",
                       style='b', pad='1', start='\n')
            printGreen(f"""delete""",
                       style='b', pad='1', start='\n')
            printGreen(f"""developer""",
                       style='b', pad='1', start='\n')
            printGreen(f"""theme [--parrot^/--normal]""",
                       style='b', pad='1', start='\n')
            printGreen(f"""clear""",
                       style='b', pad='1', start='\n')
            printGreen(f"""exit""",
                       style='b', pad='1', start='\n')
        elif self.get_command_at_index(2) == "--help":
            Main.help_with_help()
            if self.get_command_length() > 3:
                self.command = (
                    "command " + self.command.split(" ")[3]).strip()
                self.Error()
        else:
            Main.help_with_help()

    def handle_exit_commands(self):
        """Method handle_exit_commands() handles the 'exit' commands
        it calls the python's exit() function once it confirms that
        the given command is exactly a 'exit' command, it also checks
        for the flag that is given with the 'exit' command is an actual
        'exit' flag. We does a lot of argument parsing in this function
        as you can see this is to fetch the right flag and if not found
        raise an error.
        """
        if self.get_command_at_index(1) == "exit":
            printGreen(f"""Piece""", style='b', pad='1')
            sys.exit()
        elif self.get_command_at_index(2) == "--help":
            Main.help_with_exit()
            if self.get_command_length() > 3:
                self.command = (
                    "command " + self.get_command_at_index(3)).strip()
                self.Error()
        else:
            Main.help_with_exit()

    def Error(self):
        """Method Error() gets called when the entered command
        is not recognized. We say 'self.command[8:]' because this
        way we are triming the 'command ' from the entered command
        because we don't want to confuse the user by showing him/her
        what is going in the background.
        """
        if self.command:
            printRed(
                f"""`{self.command[8:]}` is not recognized as an internal command.""", style='b', pad='1')

    def slice_keyword(self):
        try:
            return self.command.split(" ")[2][self.command.split(" ")[2].find('"')+1:self.command.split(" ")[2].rfind('"')]
        except IndexError:
            return None

    def get_email(self):
        """
        Method check_email()
        """
        email = self.slice_keyword()

        if re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$", email):
            return email
        elif re.search(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$", email):
            return email
        else:
            return False

    def if_password_given(self):
        if re.search(r'"[a-zA-z0-9~`!@#\$%\^&\*\(\)_\+=-\\\|\[\]\{\}\"\'\?<>,\.:;\/]*"', self.command.split(" ")[2].strip()):
            return True
        return False

    def handle_configs(self):
        """Method handle_configs() basically saves the user's configurations
        that are passed by hitting the command `config.user.email/password`
        or `config.job/keywords/location`. We use re.compile() and re.search()
        method here to find the pattern in the command. We does a lot of argument
        parsing in this function as you can see this is to fetch the right
        commands and flags and if not found raise an error.
        """
        if self.get_command_length() <= 2 or self.get_command_length() <= 3:
            if "config.user.password" == self.get_command_at_index(1):
                self.data["user_password"] = getpass.getpass(
                    prompt=" Password: ")
                if self.get_command_at_index(2) == "--cached":
                    self.store_cache()
                    return
                return

        if re.compile(r"(config\.user\.email)", re.IGNORECASE).search(self.command):
            email = self.get_email()
            if email:
                self.data["user_email"] = email
                if self.get_command_at_index(3) == "--cached":
                    self.store_cache()
                    self.command = "command config.user.password --cached"
                else:
                    self.command = "command config.user.password"
                self.handle_configs()
                return
            else:
                printRed(
                    f"""'{self.command.split(" ")[1].strip()}' is not a valid email address!""",
                    style='b', pad='1')
                return

        elif "config.user.password" == self.get_command_at_index(1):
            self.data["user_password"] = self.slice_keyword()
            if self.get_command_at_index(3) == "--cached":
                self.store_cache()
            return

        elif re.compile(r"(config\.job\.keywords)=\w+", re.IGNORECASE).search(self.command):
            self.data["job_keywords"] = self.command[self.command.find(
                "=")+1:].strip()
            return

        elif re.compile(r"(config\.job\.location)=\w+", re.IGNORECASE).search(self.command):
            self.data["job_location"] = self.command[self.command.find(
                "=")+1:].strip()
            return

        else:
            Main.help_with_configs()
            return

    def handle_commands(self):
        """Method handle_commands() does the actually handling of the commands
        entered, we first find pattern for 'configuration' commands using the
        re.compile() and re.search() method, which finds the pattern in the
        entered command and calls 'handle_configs()' method if it finds any
        match if not it calls the functions according to the commands entered
        and if still does not find any function call for the entered command it
        just hits the self.Error() method.

        If you are really confused about what I'm doing in the else clause
        then here's the explaination -> get() method of dictionary data type
        returns value of passed argument if it is present in dictionary
        otherwise second argument will be assigned as default value of passed
        argument. (You remember the switch statement in C, C++, Javascript ...)
        """
        _config_regex_ = re.compile(
            r"(config\.user\.email)|(config\.user\.password)|(config\.job\.keywords)|(config\.job\.location)", re.IGNORECASE)

        if _config_regex_.search(self.get_command_at_index(1)):
            self.handle_configs()
        else:
            self.commands.get(self.command.split(" ")[1], self.Error)()

    def run(self):
        """Method run() runs a infinite loop and starts the `cli`
        (Command Line Interface) and it actually starts listening
        to the commands and then it calls the function handle_commands()
        which handles the commands.

        We first get the command and add 'command ' in it this way we
        can handle the commands by accessing their position in list.
        Then we call function handle commands that is going to perform
        operations as per command.
        """
        while True:
            self.command = ("command " + self._input()).strip()
            self.handle_commands() if self.get_command_length() > 1 else False


"""Execute program"""
if __name__ == "__main__":
    Main().run()
